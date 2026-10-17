"""Bura (Burkozel): 2 kishilik karta o'yini, Vercel uchun moslangan versiya.

Vercel serverlari doim ishlab turmaydi va WebSocket'ni qo'llamaydi, shuning uchun:
  * sayt serverdan har soniyada holatni so'raydi (polling);
  * xonalar va o'yin holati Upstash Redis'da saqlanadi (bepul tarif yetadi).

Vercel'da Redis ulash: Project -> Storage -> Upstash Redis (Marketplace) -> Connect.
U KV_REST_API_URL va KV_REST_API_TOKEN o'zgaruvchilarini o'zi qo'shadi.

Muhit o'zgaruvchilari:
  ADMIN_CODE   profil kodi; kiritgan o'yinchiga eng kuchli kartalar tushadi (maxfiy so'z qo'ying)
  HAND_SIZE    qo'ldagi kartalar soni (default 4)
  MATCH_LIMIT  o'yin necha balgacha boradi, yetgan yutqazadi (default 12)
  BURA_PEN     Bura (maxsus qo'l) uchun raqibga beriladigan bal (default 4)
Kompyuteringizda Redis'siz ham ishlaydi (xotirada saqlaydi): python main.py
"""
import itertools
import json
import os
import random
import time
import urllib.request

from flask import Flask, Response, jsonify, request

from page import HTML

ADMIN_CODE = os.getenv("ADMIN_CODE", "admin")
HAND_SIZE = int(os.getenv("HAND_SIZE", "4"))
MATCH_LIMIT = int(os.getenv("MATCH_LIMIT", "12"))
BURA_PEN = int(os.getenv("BURA_PEN", "4"))
BOT_MIN = float(os.getenv("BOT_MIN", "1.0"))
BOT_MAX = float(os.getenv("BOT_MAX", "1.9"))
REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL") or os.getenv("KV_REST_API_URL")
REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN") or os.getenv("KV_REST_API_TOKEN")
ON_VERCEL = bool(os.getenv("VERCEL"))
GAME_TTL = 6 * 3600
ROOM_TTL = 900
SEEN_TTL = 60

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=None)

# ------------------------------------------------------------ Redis

_mem = {}


def _mem_cmd(*a):
    now = time.time()
    for k in [k for k, (_, exp) in _mem.items() if exp and exp < now]:
        del _mem[k]
    op = a[0].upper()
    if op == "GET":
        v = _mem.get(a[1])
        return v[0] if v else None
    if op == "DEL":
        return 1 if _mem.pop(a[1], None) else 0
    if op == "SET":
        key, val, rest = a[1], a[2], list(a[3:])
        up = [x.upper() for x in rest]
        if "NX" in up and key in _mem:
            return None
        exp = now + int(rest[up.index("EX") + 1]) if "EX" in up else 0
        _mem[key] = (val, exp)
        return "OK"
    raise ValueError(op)


def rcmd(*args):
    args = [str(x) for x in args]
    if not REDIS_URL:
        return _mem_cmd(*args)
    req = urllib.request.Request(
        REDIS_URL, data=json.dumps(args).encode(),
        headers={"Authorization": "Bearer " + REDIS_TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=6) as r:
        return json.load(r).get("result")


def load(gid):
    raw = rcmd("GET", f"game:{gid}")
    return Game(json.loads(raw)) if raw else None


def save(gid, g):
    rcmd("SET", f"game:{gid}", json.dumps(g.dump()), "EX", GAME_TTL)


# ------------------------------------------------------------ o'yin qoidalari

# Karta id: 0..35. mast = id // 9, kuch = id % 9  (6 7 8 9 J Q K 10 A)
POINTS = [0, 0, 0, 0, 2, 3, 4, 10, 11]


def suit(c): return c // 9
def strength(c): return c % 9
def pts(c): return POINTS[c % 9]


def beats(d, a, trump):
    if suit(d) == suit(a):
        return strength(d) > strength(a)
    return suit(d) == trump and suit(a) != trump


def can_beat(att, dfn, trump):
    for perm in itertools.permutations(dfn):
        if all(beats(d, a, trump) for d, a in zip(perm, att)):
            return True
    return False


FIELDS = ["players", "deck", "trump_card", "trump", "hands", "scores", "table", "last",
          "result", "boost", "turn", "phase", "bot_at", "ver", "made", "pen", "rid", "round"]


class Game:
    def __init__(self, data):
        self.__dict__.update(data)
        for k, v in (("pen", [0, 0]), ("rid", 0), ("round", 0)):
            if not hasattr(self, k):
                setattr(self, k, v)

    def dump(self):
        return {k: getattr(self, k) for k in FIELDS}

    @classmethod
    def create(cls, players):
        g = cls({"players": players, "ver": 0, "made": time.time()})
        g.new_round(random.randint(0, 1))
        return g

    def new_round(self, first):
        deck = list(range(36))
        random.shuffle(deck)
        self.deck = deck
        self.trump_card = deck[-1]          # pastki karta kozir, oxirida olinadi
        self.trump = suit(self.trump_card)
        self.hands = [[], []]
        self.scores = [0, 0]
        self.table = []
        self.last = None
        self.result = None
        a, b = self.players[0]["admin"], self.players[1]["admin"]
        self.boost = [a and not b, b and not a]   # ikkalasi admin bo'lsa oddiy o'yin
        self.turn = first
        self.phase = "attack"
        self.rid += 1
        self.round += 1
        self.refill(first)
        self.refill(1 - first)
        kinds = [self.special_kind(h) for h in self.hands]
        if kinds[0] and kinds[1]:
            kinds = [None, None]          # ikkalasida bo'lsa, oddiy o'ynaladi
        for s in (0, 1):
            if kinds[s]:
                add = [0, 0]
                add[1 - s] = BURA_PEN
                self.end_round(s, "Bura: " + kinds[s], add, special=True, hand=list(self.hands[s]))
                break
        self.ver = getattr(self, "ver", 0) + 1
        self.arm()

    def special_kind(self, hand):
        """Dastlabki qo'l maxsus bo'lsa, o'yin yurishsiz tugaydi (Bura)."""
        if len(hand) != HAND_SIZE or HAND_SIZE < 4:
            return None
        if all(suit(c) == self.trump for c in hand):
            return "hammasi kozir"
        r = [strength(c) for c in hand]
        if all(x >= 7 for x in r):                  # faqat tuz (8) va o'nlik (7) dan iborat qo'l
            a, t = r.count(8), r.count(7)
            if t == 0:
                return f"{a} ta tuz"
            if a == 0:
                return f"{t} ta o'nlik"
            return f"{a} ta tuz va {t} ta o'nlik"
        return None

    def refill(self, seat):
        h = self.hands[seat]
        while len(h) < HAND_SIZE and self.deck:
            if self.boost[seat] and len(self.deck) > 1:
                cands = self.deck[:-1]
                if len(h) == HAND_SIZE - 1 and all(suit(c) == self.trump for c in h):
                    cands = [c for c in cands if suit(c) != self.trump] or cands
                best = max(cands, key=lambda c: (suit(c) == self.trump) * 100 + strength(c))
                self.deck.remove(best)
                h.append(best)
            elif self.boost[1 - seat] and self.players[seat]["bot"] and len(self.deck) > 1:
                worst = min(self.deck[:-1], key=lambda c: (suit(c) == self.trump) * 100 + strength(c))
                self.deck.remove(worst)      # admin botga qarshi o'ynasa, bot zaif kartalar oladi
                h.append(worst)
            else:
                h.append(self.deck.pop(0))

    def actor(self):
        return self.turn if self.phase == "attack" else 1 - self.turn

    def end_round(self, winner, why, add, special=False, hand=None):
        """Raund tugadi: yutqazgan o'yinchiga bal (jarima) yoziladi, 12 ga yetgan o'yinni yutqazadi."""
        self.pen = [self.pen[0] + add[0], self.pen[1] + add[1]]
        over = max(self.pen) >= MATCH_LIMIT
        mw = None
        if over and self.pen[0] != self.pen[1]:
            mw = 0 if self.pen[0] < self.pen[1] else 1
        self.result = {"winner": winner, "why": why, "add": add, "special": special,
                       "hand": hand or [], "match": {"over": over, "winner": mw}}

    def match_over(self):
        return bool(self.result and self.result.get("match", {}).get("over"))

    def advance(self):
        """Keyingi raund (yoki o'yin tugagan bo'lsa yangi o'yin). Raundni yutqazgan boshlaydi."""
        r = self.result
        if r and r.get("match", {}).get("over"):
            self.pen = [0, 0]
            self.round = 0
            first = random.randint(0, 1)
        else:
            w = r.get("winner") if r else None
            first = (1 - w) if w is not None else random.randint(0, 1)
        self.new_round(first)

    def arm(self):
        if not self.result and self.players[self.actor()]["bot"]:
            self.bot_at = time.time() + random.uniform(BOT_MIN, BOT_MAX)
        else:
            self.bot_at = 0

    def forfeit(self, leaver):
        if not self.match_over():
            self.result = {"winner": 1 - leaver, "why": "Raqib o'yindan chiqdi", "add": [0, 0],
                           "special": False, "hand": [],
                           "match": {"over": True, "winner": 1 - leaver}}
            self.ver += 1
            self.bot_at = 0

    def bot_step(self, now):
        if self.result or not self.bot_at or now < self.bot_at:
            return False
        s = self.actor()
        if not self.players[s]["bot"]:
            return False
        return self.play(s, bot_move(self, s)) is None

    def play(self, seat, cards):
        err = self._play(seat, cards)
        if err is None:
            self.ver += 1
            self.arm()
        return err

    def _play(self, seat, cards):
        if self.result:
            return "O'yin tugagan"
        if seat != self.actor():
            return "Navbat sizda emas"
        if (not cards or len(set(cards)) != len(cards)
                or any(c not in self.hands[seat] for c in cards)):
            return "Noto'g'ri kartalar"
        if self.phase == "attack":
            if len({suit(c) for c in cards}) != 1:
                return "Bir xil mastdagi kartalarni tanlang"
            if len(cards) > len(self.hands[1 - seat]):
                return "Raqibda bunchalik karta yo'q"
            for c in cards:
                self.hands[seat].remove(c)
            self.table = list(cards)
            self.phase = "defend"
            return None
        if len(cards) != len(self.table):
            return f"Aynan {len(self.table)} ta karta tashlang"
        att, atk = self.table, self.turn
        for c in cards:
            self.hands[seat].remove(c)
        winner = seat if can_beat(att, cards, self.trump) else atk
        total = sum(pts(c) for c in att + list(cards))
        self.scores[winner] += total
        self.last = {"att": att, "def": list(cards), "winner": winner, "pts": total}
        self.table = []
        self.refill(winner)
        self.refill(1 - winner)
        self.turn = winner
        self.phase = "attack"
        if not self.hands[winner] or not self.hands[1 - winner]:
            a, b = self.scores
            if a == b:
                self.end_round(None, f"Durang, {a}:{b}", [0, 0])
            else:
                w = 0 if a > b else 1
                hi, lo = max(a, b), min(a, b)
                # yutqazgan jarimasi: 61-90 ochko -> 2 bal, 91-119 -> 4 bal, hamma ochko (lo=0) -> 6 bal
                add = [0, 0]
                add[1 - w] = 6 if lo == 0 else (4 if hi >= 91 else 2)
                self.end_round(w, f"Hisob {hi}:{lo}", add)
        return None

    def state_for(self, seat, gid):
        over = self.result is not None
        opp = self.players[1 - seat]
        res = None
        if self.result:
            res = dict(self.result)
            add = res.get("add", [0, 0])
            res["add"] = [add[seat], add[1 - seat]]        # [menga, raqibga]
        return {
            "gid": gid, "v": self.ver, "rid": self.rid, "round": self.round, "limit": MATCH_LIMIT,
            "pen": [self.pen[seat], self.pen[1 - seat]],
            "mode": "bot" if opp["bot"] else "online",
            "me": seat, "opp": opp["name"],
            "hand": self.hands[seat], "oppN": len(self.hands[1 - seat]),
            "deckN": len(self.deck), "trump": self.trump,
            "trumpCard": self.trump_card if self.trump_card in self.deck else None,
            "actor": self.actor(), "phase": self.phase, "table": self.table,
            "myScore": self.scores[seat], "scores": self.scores if over else None,
            "last": self.last, "result": res,
        }


def cost(c, trump):
    return strength(c) + (10 if suit(c) == trump else 0)


def bot_move(g, seat):
    hand, trump = g.hands[seat], g.trump
    if g.phase == "attack":
        opp_n = len(g.hands[1 - seat])
        by = {}
        for c in hand:
            by.setdefault(suit(c), []).append(c)
        order = sorted(by, key=lambda s: (s == trump, min(strength(c) for c in by[s])))
        s = order[0]
        cards = sorted(by[s], key=strength)
        strong = [c for c in cards if strength(c) >= 6]
        if s != trump and 2 <= len(strong) <= opp_n and random.random() < 0.6:
            return strong
        return cards[:1]
    att, n = g.table, len(g.table)
    in_play = sum(pts(c) for c in att)
    combos = list(itertools.combinations(hand, n))
    winning = [cb for cb in combos if can_beat(att, cb, trump)]
    cheapest = min(combos, key=lambda cb: sum(pts(c) * 2 + cost(c, trump) for c in cb))
    if winning:
        best = min(winning, key=lambda cb: sum(cost(c, trump) for c in cb))
        if in_play >= 10 or sum(cost(c, trump) for c in best) <= 8 or random.random() < 0.5:
            return list(best)
    return list(cheapest)


# ------------------------------------------------------------ API

BOT_NAMES = ["Rustam", "Dilshod", "Jasur", "Sardor", "Aziz", "Bobur"]


def me_from(d, pid):
    name = (str(d.get("name") or "").strip() or "Mehmon")[:20]
    code = str(d.get("code") or "")[:64]
    return {"pid": pid, "name": name, "admin": bool(ADMIN_CODE) and code == ADMIN_CODE, "bot": False}


def new_gid():
    return "%016x" % random.getrandbits(64)


def touch(gid, seat):
    rcmd("SET", f"seen:{gid}:{seat}", 1, "EX", SEEN_TTL)


def start(gid, players):
    g = Game.create(players)
    save(gid, g)
    for s, p in enumerate(players):
        if not p["bot"]:
            rcmd("SET", f"p:{p['pid']}", gid, "EX", GAME_TTL)
            touch(gid, s)
    return g


def game_resp(g, seat, gid, **extra):
    return dict({"status": "game", "state": g.state_for(seat, gid)}, **extra)


def seat_of(g, pid):
    for s, p in enumerate(g.players):
        if p["pid"] == pid:
            return s
    return None


def h_bot(d, pid):
    me = me_from(d, pid)
    bot = {"pid": "", "name": random.choice([n for n in BOT_NAMES if n != me["name"]]) + " (bot)",
           "admin": False, "bot": True}
    gid = new_gid()
    g = start(gid, [me, bot])
    return game_resp(g, 0, gid)


def h_create(d, pid):
    me = me_from(d, pid)
    old = rcmd("GET", f"pr:{pid}")
    if old:
        rcmd("DEL", f"room:{old}")
    for _ in range(30):
        code = f"{random.randint(0, 9999):04d}"
        if rcmd("SET", f"room:{code}", json.dumps(me), "NX", "EX", ROOM_TTL):
            rcmd("SET", f"pr:{pid}", code, "EX", ROOM_TTL)
            return {"status": "waiting", "room": code}
    return {"error": "Hozir baza ochib bo'lmadi, qayta urinib ko'ring"}


def h_join(d, pid):
    code = str(d.get("room", "")).strip()
    raw = rcmd("GET", f"room:{code}") if code.isdigit() and len(code) == 4 else None
    host = json.loads(raw) if raw else None
    if not host or host["pid"] == pid:
        return {"error": "Bunday baza topilmadi"}
    if rcmd("DEL", f"room:{code}") != 1:        # boshqa kimdir oldinroq kirib ulgurgan
        return {"error": "Bunday baza topilmadi"}
    rcmd("DEL", f"pr:{host['pid']}")
    gid = new_gid()
    players = [host, me_from(d, pid)]
    random.shuffle(players)
    g = start(gid, players)
    return game_resp(g, seat_of(g, pid), gid)


def h_state(d, pid):
    gid = d.get("gid") or rcmd("GET", f"p:{pid}")
    if not gid:
        room = str(d.get("room") or rcmd("GET", f"pr:{pid}") or "")
        if room and rcmd("GET", f"room:{room}"):
            return {"status": "waiting", "room": room}
        return {"status": "lobby"}
    g = load(gid)
    seat = seat_of(g, pid) if g else None
    if seat is None:
        rcmd("DEL", f"p:{pid}")
        return {"status": "lobby", "msg": "O'yin tugagan yoki topilmadi"}
    changed = g.bot_step(time.time())
    if d.get("hb"):
        touch(gid, seat)
        opp = g.players[1 - seat]
        if (not opp["bot"] and not g.match_over() and time.time() - g.made > SEEN_TTL
                and not rcmd("GET", f"seen:{gid}:{1 - seat}")):
            g.forfeit(1 - seat)
            changed = True
    if changed:
        save(gid, g)
    if d.get("gid") == gid and d.get("v") == g.ver:
        return {"status": "game", "same": True}
    return game_resp(g, seat, gid)


def h_play(d, pid):
    gid = d.get("gid")
    g = load(gid) if gid else None
    seat = seat_of(g, pid) if g else None
    if seat is None:
        return {"status": "lobby", "msg": "O'yin topilmadi"}
    try:
        cards = [int(x) for x in d.get("cards", [])]
    except (TypeError, ValueError):
        return {"error": "Noto'g'ri kartalar"}
    err = g.play(seat, cards)
    if err:
        return {"error": err}
    save(gid, g)
    return game_resp(g, seat, gid)


def h_again(d, pid):
    gid = d.get("gid")
    g = load(gid) if gid else None
    seat = seat_of(g, pid) if g else None
    if seat is None or not g.result:
        return {"status": "lobby"} if seat is None else game_resp(g, seat, gid)
    opp = g.players[1 - seat]
    if opp["bot"] or rcmd("GET", f"again:{gid}:{1 - seat}"):
        rcmd("DEL", f"again:{gid}:{1 - seat}")
        g.advance()
        save(gid, g)
        return game_resp(g, seat, gid)
    rcmd("SET", f"again:{gid}:{seat}", 1, "EX", 600)
    return {"status": "game", "same": True, "waitAgain": True}


def h_leave(d, pid):
    gid = d.get("gid") or rcmd("GET", f"p:{pid}")
    if gid:
        g = load(gid)
        seat = seat_of(g, pid) if g else None
        if g and seat is not None and not g.players[1 - seat]["bot"]:
            g.forfeit(seat)
            save(gid, g)
    room = rcmd("GET", f"pr:{pid}")
    if room:
        rcmd("DEL", f"room:{room}")
        rcmd("DEL", f"pr:{pid}")
    rcmd("DEL", f"p:{pid}")
    return {"status": "lobby"}


HANDLERS = {"bot": h_bot, "create": h_create, "join": h_join, "state": h_state,
            "play": h_play, "again": h_again, "leave": h_leave}


@app.post("/api/<action>")
def api(action):
    fn = HANDLERS.get(action)
    d = request.get_json(silent=True) or {}
    pid = str(d.get("pid", ""))[:64]
    if not fn or len(pid) < 8:
        return jsonify(error="Noto'g'ri so'rov"), 400
    if ON_VERCEL and not REDIS_URL:
        return jsonify(error="Redis ulanmagan: Vercel'da Storage bo'limidan Upstash Redis qo'shing")
    try:
        return jsonify(fn(d, pid))
    except Exception as e:           # noqa
        app.logger.exception("api xatosi")
        return jsonify(error="Server xatosi, qayta urinib ko'ring"), 500


@app.get("/")
def index():
    return Response(HTML, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
