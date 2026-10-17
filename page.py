# Sayt sahifasi (HTML). Alohida fayl sifatida emas, Python moduli sifatida saqlanadi,
# shunda Vercel uni funksiya bilan birga albatta yuklaydi.
HTML = r'''<!doctype html>
<html lang="uz">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Bura</title>
<style>
:root{
  --felt:#1b4535; --felt-dark:#0f291f; --wood:#34200e; --wood-light:#5c3b1c;
  --cream:#f2ead6; --ink:#17130f; --red:#a3261d; --brass:#c9a04a; --muted:#a9bcaf;
  --serif:Georgia,"Times New Roman",serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%;margin:0}
body{
  font-family:var(--sans);color:var(--cream);background-color:var(--felt);
  background-image:
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .32 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"),
    radial-gradient(ellipse at 50% 38%,rgba(255,255,255,.08),rgba(0,0,0,.42) 88%);
  padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
}
[hidden]{display:none!important}
button,input{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--brass);outline-offset:2px}

.btn{background:var(--cream);color:var(--ink);border:0;border-radius:3px;padding:12px 18px;font-weight:600;cursor:pointer;
  box-shadow:0 2px 0 rgba(0,0,0,.45)}
.btn:active{transform:translateY(1px);box-shadow:0 1px 0 rgba(0,0,0,.45)}
.btn.brass{background:var(--brass)}
.btn.quiet{background:transparent;color:var(--cream);box-shadow:inset 0 0 0 1px rgba(242,234,214,.35)}
.btn:disabled{opacity:.4;cursor:default;transform:none}
input{background:rgba(0,0,0,.28);border:1px solid rgba(242,234,214,.28);border-radius:3px;padding:11px 12px;width:100%}
input::placeholder{color:rgba(242,234,214,.5)}
#conn{position:fixed;top:0;left:0;right:0;background:var(--red);padding:6px;text-align:center;font-size:14px;z-index:30}
.snd{background:transparent;border:1px solid rgba(242,234,214,.3);border-radius:3px;width:34px;height:30px;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
.snd svg{width:18px;height:18px;fill:none;stroke:var(--cream);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.snd.off .wave{display:none}

/* ---------- lobby ---------- */
.page{min-height:100%;padding:34px 22px 40px;max-width:520px;margin:0 auto;position:relative}
.head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
h1{font-family:var(--serif);font-size:56px;line-height:1;margin:0 0 6px;font-weight:700}
.lead{margin:0 0 26px;color:var(--muted);line-height:1.5;max-width:32ch}
.hero{--cw:50px;position:relative;width:120px;height:92px;flex:none;margin-top:4px}
.hero .card{position:absolute;bottom:0;left:50%;margin-left:-25px;transform-origin:50% 130%}
.hero-tools{position:absolute;top:14px;right:18px}
.block{padding:18px 0;border-top:1px solid rgba(242,234,214,.2)}
.block h2{font-family:var(--serif);font-size:20px;margin:0 0 4px;font-weight:700}
.block p{margin:0 0 12px;color:var(--muted);font-size:15px;line-height:1.45}
.row{display:flex;gap:8px;align-items:stretch}
.row input{min-width:0}
.field{margin-bottom:22px}
.field label{display:block;margin-bottom:6px;font-size:14px;color:var(--muted)}
#err{min-height:22px;color:#f0b4a8;margin-top:10px}
.codefield{margin-top:18px;font-size:13px}
.codefield label{display:block;margin-bottom:5px;color:var(--muted)}
.codefield input{max-width:220px;padding:8px 10px;font-size:14px}
details.rules{border-top:1px solid rgba(242,234,214,.2);padding:14px 0 0;margin-top:22px;color:var(--muted);font-size:14px;line-height:1.55}
details.rules summary{cursor:pointer;color:var(--cream);font-family:var(--serif);font-size:17px;margin-bottom:8px}
details.rules ul{margin:6px 0 10px;padding-left:18px}

/* ---------- baza kutish ---------- */
#wait .big{font-family:var(--serif);font-size:88px;letter-spacing:.12em;margin:18px 0 8px;font-weight:700;color:var(--brass);text-shadow:0 3px 0 rgba(0,0,0,.35)}
#wait p{color:var(--muted);line-height:1.5;max-width:36ch}

/* ---------- stol ---------- */
#game{height:100vh;height:100dvh;display:flex;flex-direction:column;
  border:clamp(8px,2vw,16px) solid var(--wood);
  box-shadow:inset 0 0 0 2px var(--wood-light),inset 0 0 70px rgba(0,0,0,.6)}
.top{display:flex;justify-content:space-between;align-items:flex-start;padding:10px 14px 0;gap:8px}
.side{display:flex;flex-direction:column;min-width:0}
.side.right{align-items:flex-end}
.nm{font-family:var(--serif);font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:34vw}
.dots{display:flex;gap:4px;margin-top:6px}
.dots i{width:9px;height:9px;border-radius:50%;border:1px solid rgba(242,234,214,.5);background:transparent;transition:background .3s}
.dots i.on{background:#c8412f;border-color:#c8412f;box-shadow:0 0 6px rgba(200,65,47,.6)}
.cap{font-size:11px;color:var(--muted);margin-top:3px}
.mid-top{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:12px;color:var(--muted);white-space:nowrap}
.oppzone{display:flex;justify-content:center;padding-top:6px;height:calc(var(--cws)*1.4*.62 + 12px)}
.oppzone .fan{display:flex}
.oppzone .card{margin-left:calc(var(--cws)*-.5)}
.oppzone .card:first-child{margin-left:0}
.oppzone .card.dealt{animation:oppIn .4s ease-out backwards;animation-delay:calc(var(--i)*.08s)}
.mid{flex:1;min-height:0;display:flex;align-items:center;justify-content:space-around;padding:0 10px;gap:8px}
.deckwrap{position:relative;width:calc(var(--cws)*2.2);height:calc(var(--cws)*1.4);flex:none}
.deckwrap .card{position:absolute;top:0}
.deckwrap .stack{left:0;z-index:2}
.deckwrap .stack.two{box-shadow:2px 2px 0 #c9bfa5,3px 3px 0 rgba(0,0,0,.5),5px 6px 8px rgba(0,0,0,.4)}
.deckwrap .under{left:calc(var(--cws)*.95);transform:rotate(90deg);z-index:1}
.deckwrap .suitonly{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.deckwrap .suitonly svg{width:calc(var(--cws)*.8);height:calc(var(--cws)*.8);fill:currentColor;filter:drop-shadow(0 2px 2px rgba(0,0,0,.4))}
.deckwrap .suitonly.red{color:#d4574c}
.deckwrap .suitonly.blk{color:var(--cream)}
.deckn{position:absolute;bottom:-20px;left:0;font-size:13px;color:var(--muted)}
.play{display:flex;flex-direction:column;align-items:center;gap:8px;min-width:0}
.trick{display:flex;min-height:calc(var(--cws)*1.4+6px);align-items:center;justify-content:center;flex-wrap:wrap}
.trick .card{margin:0 -4px;transform:rotate(var(--rot,0deg))}
.trick .card.fresh{animation:throwIn .3s ease-out backwards}
.trick.old .card{opacity:.5}
.lasttext{font-size:13px;color:var(--muted);min-height:18px;text-align:center}
.meta{display:flex;justify-content:center;gap:16px;font-size:13px;color:var(--muted);min-height:18px}
.meta b{color:var(--cream);font-family:var(--serif);font-size:15px}
.msg{text-align:center;padding:2px 16px 4px;min-height:26px;color:var(--brass);font-size:15px}
.handzone{display:flex;justify-content:center;align-items:flex-end;padding:8px 6px 6px;min-height:calc(var(--cw)*1.4 + 32px)}
.hand{display:flex;padding-top:20px}
.hand .card{margin-left:calc(var(--cw)*-.1);cursor:pointer;transform-origin:50% 120%;
  transform:translateY(var(--y,0)) rotate(var(--r,0deg));transition:transform .13s}
.hand .card:first-child{margin-left:0}
.hand .card.sel{transform:translateY(calc(var(--y,0px) - 20px)) rotate(var(--r,0deg))}
.hand .card.dealt{animation:dealIn .5s cubic-bezier(.2,.8,.3,1) backwards;animation-delay:calc(var(--i)*.1s)}
.hand.locked .card{cursor:default}
.actions{display:flex;gap:10px;justify-content:center;padding:6px 14px 14px}
.actions .btn{min-width:130px}
@keyframes dealIn{from{transform:translate(-26vw,-52vh) rotate(-40deg) scale(.55);opacity:0}to{transform:translateY(var(--y,0)) rotate(var(--r,0deg));opacity:1}}
@keyframes oppIn{from{transform:translateY(-60px);opacity:0}to{transform:none;opacity:1}}
@keyframes throwIn{from{transform:translateY(var(--fy,90px)) rotate(calc(var(--rot,0deg) + 24deg)) scale(1.2);opacity:0}to{transform:rotate(var(--rot,0deg));opacity:1}}

/* ---------- kartalar ---------- */
.card{--cw:inherit;position:relative;flex:none;width:var(--cw);height:calc(var(--cw)*1.4);font-size:calc(var(--cw)/10);
  border-radius:calc(var(--cw)*.07);background:linear-gradient(160deg,#f7f1e0,#eadfc5);color:var(--ink);
  box-shadow:0 1px 0 #fff8 inset,0 1px 1px rgba(0,0,0,.5),0 3px 6px rgba(0,0,0,.35);user-select:none}
.card.red{color:var(--red)}
.card .idx{position:absolute;display:flex;flex-direction:column;align-items:center;line-height:1;width:2.6em}
.card .idx b{font-family:var(--serif);font-size:1.6em;font-weight:700;letter-spacing:-.06em}
.card .idx svg{width:1.25em;height:1.25em;fill:currentColor;margin-top:.12em}
.card .tl{top:.55em;left:.45em}
.card .br{bottom:.55em;right:.45em;transform:rotate(180deg)}
.card .field{position:absolute;inset:0}
.card .pip{position:absolute;width:19%;aspect-ratio:1;transform:translate(-50%,-50%)}
.card .pip.flip{transform:translate(-50%,-50%) rotate(180deg)}
.card .pip.big{width:44%}
.card .pip svg{display:block;width:100%;height:100%;fill:currentColor}
.card .royal{position:absolute;left:25%;right:25%;top:11%;bottom:11%;border:1px solid currentColor;display:flex;flex-direction:column;
  align-items:center;justify-content:space-between;padding:.5em 0;
  background:repeating-linear-gradient(135deg,rgba(0,0,0,.05) 0 2px,transparent 2px 6px)}
.card .royal b{font-family:var(--serif);font-size:3.4em;line-height:1;font-weight:700}
.card .royal svg{width:1.7em;height:1.7em;fill:currentColor}
.card .royal svg:last-child{transform:rotate(180deg)}
.card.back{background:#7c1d1a;border:calc(var(--cw)*.06) solid #f2ead6}
.card.back::after{content:"";position:absolute;inset:calc(var(--cw)*.05);border:1px solid rgba(242,234,214,.7);
  background:
    repeating-linear-gradient(45deg,rgba(242,234,214,.28) 0 1px,transparent 1px 7px),
    repeating-linear-gradient(-45deg,rgba(242,234,214,.28) 0 1px,transparent 1px 7px)}

/* ---------- natija va Bura ---------- */
#over{position:fixed;inset:0;background:rgba(8,18,13,.82);display:flex;align-items:center;justify-content:center;padding:24px;z-index:10}
#over .box{background:var(--felt-dark);border:1px solid rgba(242,234,214,.3);border-radius:4px;padding:26px 24px;max-width:350px;width:100%;box-shadow:0 12px 40px rgba(0,0,0,.6);animation:rise .3s ease-out}
#over h2{font-family:var(--serif);font-size:29px;margin:0 0 8px}
#over p{margin:5px 0;color:var(--muted);line-height:1.4}
#over p.pen{color:var(--cream)}
#over p.tot{margin-top:10px;padding-top:10px;border-top:1px solid rgba(242,234,214,.2)}
#over .row{margin-top:18px}
#over .row .btn{flex:1}
#bura{position:fixed;inset:0;z-index:20;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle,rgba(40,28,6,.82),rgba(6,12,9,.92));animation:fade .25s}
.bura-box{text-align:center;padding:20px}
.bura-title{font-family:var(--serif);font-size:clamp(64px,21vw,124px);font-weight:700;letter-spacing:.06em;color:var(--brass);
  text-shadow:0 0 34px rgba(201,160,74,.6),0 5px 0 #6b4f17;animation:pop .65s cubic-bezier(.2,1.6,.4,1)}
.bura-sub{font-size:19px;margin:6px 0 20px;color:var(--cream)}
.bura-cards{--cw:clamp(52px,16vw,74px);display:flex;justify-content:center}
.bura-cards .card{margin-left:calc(var(--cw)*-.15);animation:throwIn .5s ease-out backwards;--fy:60px}
.bura-cards .card:first-child{margin-left:0}
@keyframes pop{from{transform:scale(.3) rotate(-8deg);opacity:0}to{transform:none;opacity:1}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes rise{from{transform:translateY(16px);opacity:0}to{transform:none;opacity:1}}

#game{--cw:clamp(60px,19vw,92px);--cws:clamp(44px,13vw,66px)}
.mid .card,.trick .card,.oppzone .card,.deckwrap .card{width:var(--cws);height:calc(var(--cws)*1.4);font-size:calc(var(--cws)/10)}
.hand .card{width:var(--cw);height:calc(var(--cw)*1.4);font-size:calc(var(--cw)/10)}
.hero .card,.bura-cards .card{width:var(--cw);height:calc(var(--cw)*1.4);font-size:calc(var(--cw)/10)}
@media(min-width:760px){#game{--cw:92px;--cws:70px}}
@media(prefers-reduced-motion:reduce){.hand .card,.hand .card.dealt,.oppzone .card.dealt,.trick .card.fresh,.bura-title,#bura,#over .box{animation:none}.hand .card{transition:none}}
</style>
</head>
<body>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="s0" viewBox="0 0 100 100"><path d="M50 4C50 4 8 38 8 62C8 78 23 86 37 79C35 89 31 94 24 97H76C69 94 65 89 63 79C77 86 92 78 92 62C92 38 50 4 50 4Z"/></symbol>
  <symbol id="s1" viewBox="0 0 100 100"><path d="M50 93C50 93 6 62 6 34C6 17 19 6 33 6C42 6 48 12 50 19C52 12 58 6 67 6C81 6 94 17 94 34C94 62 50 93 50 93Z"/></symbol>
  <symbol id="s2" viewBox="0 0 100 100"><path d="M50 3L89 50L50 97L11 50Z"/></symbol>
  <symbol id="s3" viewBox="0 0 100 100"><path d="M50 5C38 5 30 14 30 26C30 31 32 36 35 40C32 38 28 37 24 37C13 37 5 46 5 57C5 68 13 77 24 77C31 77 37 73 42 67C42 79 38 89 30 96H70C62 89 58 79 58 67C63 73 69 77 76 77C87 77 95 68 95 57C95 46 87 37 76 37C72 37 68 38 65 40C68 36 70 31 70 26C70 14 62 5 50 5Z"/></symbol>
</svg>

<div id="conn" hidden>Aloqa uzildi, qayta ulanmoqda</div>

<main class="page" id="lobby">
  <div class="hero-tools"><button class="snd" id="sndLobby" aria-label="Ovozni yoqish yoki o'chirish"></button></div>
  <div class="head">
    <div>
      <h1>Bura</h1>
      <p class="lead">Ikki kishilik karta o'yini. Botga qarshi mashq qiling yoki do'stingiz bilan onlayn o'ynang.</p>
    </div>
    <div class="hero" id="hero" aria-hidden="true"></div>
  </div>

  <div class="field">
    <label for="name">Ismingiz</label>
    <input id="name" maxlength="20" autocomplete="nickname" placeholder="Masalan, Aziz">
  </div>

  <section class="block">
    <h2>Botga qarshi</h2>
    <p>Internet orqali boshqa odam kerak emas. Bot sizga qarshi o'ynaydi.</p>
    <button class="btn brass" id="vsBot">Botga qarshi o'ynash</button>
  </section>

  <section class="block">
    <h2>Onlayn, do'st bilan</h2>
    <p>Baza oching, tizim 4 xonali raqam beradi. Do'stingiz shu raqamni kiritsa, o'yin boshlanadi.</p>
    <div class="row" style="margin-bottom:12px">
      <button class="btn" id="create">Baza ochish</button>
    </div>
    <div class="row">
      <input id="room" inputmode="numeric" pattern="[0-9]*" maxlength="4" placeholder="Baza raqami, masalan 0224" aria-label="Baza raqami">
      <button class="btn quiet" id="join">Kirish</button>
    </div>
    <div id="err" role="status"></div>
  </section>

  <details class="rules">
    <summary>Qoidalar</summary>
    <p>Har o'yinchiga 4 tadan karta beriladi. Pastki karta kozirni belgilaydi. Raund oxirida ko'proq ochko olgan yutadi, yutqazgan o'yinchiga jarima bal yoziladi. Balli <b>12</b> ga yetgan butun o'yinni yutqazadi.</p>
    <ul>
      <li>Yutgan 61 dan 90 gacha ochko olsa: raqibga 2 bal</li>
      <li>Yutgan 91 dan 119 gacha olsa: raqibga 4 bal</li>
      <li>Raqib bitta ham ochko ola olmasa: 6 bal</li>
    </ul>
    <p><b>Bura:</b> dastlabki qo'lda 4 ta karta ham tuz yoki o'nlik bo'lsa (4 tuz, 4 o'nlik, 3 tuz va o'nlik, 2 tuz va 2 o'nlik...) yoki hammasi kozir bo'lsa, kartalar o'zi tashlanadi va raund darrov tugaydi. Raqibga 4 bal yoziladi.</p>
  </details>

  <div class="codefield">
    <label for="code">Profil kodi</label>
    <input id="code" autocomplete="off" placeholder="Bo'lsa kiriting">
  </div>
</main>

<main class="page" id="wait" hidden>
  <h1>Baza ochildi</h1>
  <div class="big" id="roomCode">0000</div>
  <p>Raqibingizga shu raqamni ayting. U Onlayn bo'limida raqamni kiritishi bilan o'yin boshlanadi.</p>
  <p style="margin-top:22px"><button class="btn quiet" id="cancel">Bazani yopish</button></p>
</main>

<section id="game" hidden>
  <div class="top">
    <div class="side"><div class="nm" id="oppName"></div><div class="dots" id="oppDots"></div><div class="cap">raqib bali</div></div>
    <div class="mid-top"><span id="roundNo"></span><button class="snd" id="sndGame" aria-label="Ovozni yoqish yoki o'chirish"></button></div>
    <div class="side right"><div class="nm">Siz</div><div class="dots" id="myDots"></div><div class="cap">sizning balingiz</div></div>
  </div>
  <div class="oppzone"><div class="fan" id="oppCards"></div></div>
  <div class="mid">
    <div class="deckwrap" id="deck"></div>
    <div class="play">
      <div class="trick" id="trick"></div>
      <div class="lasttext" id="last"></div>
    </div>
  </div>
  <div class="meta"><span>Raund ochkosi <b id="myScore">0</b></span></div>
  <div class="msg" id="msg"></div>
  <div class="handzone"><div class="hand" id="hand"></div></div>
  <div class="actions">
    <button class="btn brass" id="play" disabled>Yurish</button>
    <button class="btn quiet" id="leave">Chiqish</button>
  </div>
</section>

<div id="bura" hidden><div class="bura-box">
  <div class="bura-title">BURA!</div>
  <div class="bura-sub" id="buraSub"></div>
  <div class="bura-cards" id="buraCards"></div>
</div></div>

<div id="over" hidden><div class="box">
  <h2 id="oTitle"></h2>
  <p id="oWhy"></p><p id="oScore"></p><p class="pen" id="oPen"></p><p class="tot" id="oTot"></p><p id="oWait"></p>
  <div class="row"><button class="btn brass" id="again">Keyingi raund</button><button class="btn quiet" id="exit">Chiqish</button></div>
</div></div>

<script>
const RANKS = ["6","7","8","9","J","Q","K","10","A"];
const $ = id => document.getElementById(id);
const suit = c => Math.floor(c / 9), rank = c => c % 9;
const isRed = s => s === 1 || s === 2;   // 0 qarg'a, 1 chillak, 2 g'isht, 3 xoch
const pid = localStorage.buraPid || (localStorage.buraPid =
  (window.crypto && crypto.randomUUID ? crypto.randomUUID().replace(/-/g, "") : Math.random().toString(16).slice(2) + Date.now().toString(16) + Math.random().toString(16).slice(2)));
let S = null, sel = new Set(), view = "lobby", room = null, gid = null, v = -1, busy = false, timer = null, lastHb = 0;
let animDeal = false, animThrow = false, buraUntil = 0;

$("name").value = localStorage.buraName || "";
$("code").value = localStorage.buraCode || "";

/* ---------- ovoz (hammasi brauzerning o'zida hosil qilinadi) ---------- */
const AC = window.AudioContext || window.webkitAudioContext;
let ctx = null, muted = localStorage.buraMute === "1";
function audio(){
  if (!ctx && AC) { try { ctx = new AC(); } catch (e) { ctx = null; } }
  if (ctx && ctx.state === "suspended") ctx.resume();
  return ctx;
}
function noiseBuf(c, dur){
  const n = Math.floor(c.sampleRate * dur), b = c.createBuffer(1, n, c.sampleRate), d = b.getChannelData(0);
  for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2.5);
  return b;
}
function flick(delay, vol, freq){
  if (muted) return; const c = audio(); if (!c) return;
  const t = c.currentTime + (delay || 0), s = c.createBufferSource(), f = c.createBiquadFilter(), g = c.createGain();
  s.buffer = noiseBuf(c, .09); f.type = "bandpass"; f.frequency.value = freq || 3000; f.Q.value = .8; g.gain.value = vol || .5;
  s.connect(f); f.connect(g); g.connect(c.destination); s.start(t);
}
function thump(delay, vol){
  if (muted) return; const c = audio(); if (!c) return;
  const t = c.currentTime + (delay || 0), o = c.createOscillator(), g = c.createGain();
  o.frequency.setValueAtTime(170, t); o.frequency.exponentialRampToValueAtTime(55, t + .09);
  g.gain.setValueAtTime(vol || .45, t); g.gain.exponentialRampToValueAtTime(.001, t + .12);
  o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + .13);
}
function tone(freq, delay, dur, type, vol){
  if (muted) return; const c = audio(); if (!c) return;
  const t = c.currentTime + delay, o = c.createOscillator(), g = c.createGain();
  o.type = type || "triangle"; o.frequency.value = freq;
  g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(vol || .22, t + .02); g.gain.exponentialRampToValueAtTime(.0001, t + dur);
  o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + dur + .02);
}
const sfx = {
  deal(n){ for (let i = 0; i < (n || 4) * 2; i++) flick(i * .07, .45, 2400 + Math.random() * 1400); },
  throwCard(){ flick(0, .9, 1500); thump(0, .5); },
  tick(){ flick(0, .25, 4200); },
  chime(){ tone(784, 0, .25, "sine", .18); tone(1047, .08, .3, "sine", .14); },
  low(){ tone(196, 0, .25, "sine", .16); },
  win(){ [523, 659, 784, 1047].forEach((f, i) => tone(f, i * .11, .35, "triangle", .2)); },
  lose(){ [392, 330, 262].forEach((f, i) => tone(f, i * .16, .4, "triangle", .18)); },
  bura(){
    [392, 523, 659, 784].forEach((f, i) => tone(f, i * .12, .5, "sawtooth", .12));
    [523, 659, 784, 1047].forEach(f => tone(f, .55, 1.1, "triangle", .16));
    thump(0, .7);
  }
};
function syncSound(){
  ["sndLobby", "sndGame"].forEach(id => {
    const b = $(id);
    b.classList.toggle("off", muted);
    b.innerHTML = '<svg viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor" stroke="none"/><path class="wave" d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12"/>' + (muted ? '<path d="M16 9l5 6M21 9l-5 6"/>' : '') + '</svg>';
  });
}
function toggleSound(){ muted = !muted; localStorage.buraMute = muted ? "1" : "0"; syncSound(); if (!muted) sfx.tick(); }
$("sndLobby").onclick = $("sndGame").onclick = toggleSound;
syncSound();
document.addEventListener("pointerdown", audio, {once: true});

/* ---------- aloqa ---------- */
async function api(path, extra){
  busy = true;
  try {
    localStorage.buraName = $("name").value.trim();
    localStorage.buraCode = $("code").value.trim();
    const r = await fetch("/api/" + path, {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify(Object.assign({pid, name: $("name").value.trim(), code: $("code").value.trim()}, extra || {}))
    });
    const j = await r.json();
    $("conn").hidden = true;
    return j;
  } catch (e) { $("conn").hidden = false; return null; }
  finally { busy = false; }
}

function setView(x){
  view = x;
  $("lobby").hidden = x !== "lobby";
  $("wait").hidden = x !== "wait";
  $("game").hidden = x !== "game";
  if (x !== "game"){ $("over").hidden = true; $("bura").hidden = true; }
}
function showError(msg){ if (view === "game") $("msg").textContent = msg; else $("err").textContent = msg; }

function lastKey(l){ return l ? l.att.join() + "|" + l.def.join() : ""; }
function events(old, n){
  if (!old || old.rid !== n.rid){
    animDeal = true; sfx.deal(n.hand.length);
  } else {
    if (n.table.length > old.table.length){ animThrow = true; sfx.throwCard(); }
    if (lastKey(n.last) !== lastKey(old.last)){
      animThrow = true; sfx.throwCard();
      const won = n.last && n.last.winner === n.me;
      setTimeout(() => won ? sfx.chime() : sfx.low(), 280);
    }
  }
  const had = old && old.rid === n.rid && old.result;
  if (n.result && !had){
    if (n.result.special) showBura(n);
    else setTimeout(() => (n.result.winner === n.me ? sfx.win() : (n.result.winner === null ? sfx.tick() : sfx.lose())), 600);
  }
}
function showBura(n){
  const mine = n.result.winner === n.me;
  $("buraSub").textContent = (mine ? "Sizda " : "Raqibda ") + n.result.why.replace("Bura: ", "");
  const bc = $("buraCards"); bc.replaceChildren();
  (n.result.hand || []).forEach((c, i) => { const e = cardEl(c); e.style.animationDelay = (i * .12) + "s"; bc.append(e); });
  $("bura").hidden = false; sfx.bura();
  buraUntil = Date.now() + 3300;
  setTimeout(() => { $("bura").hidden = true; render(); }, 3300);
}

function apply(j){
  if (!j) return;
  if (j.error){ showError(j.error); return; }
  if (j.status === "lobby"){
    S = null; gid = null; room = null; v = -1; setView("lobby");
    if (j.msg) $("err").textContent = j.msg;
  } else if (j.status === "waiting"){
    room = j.room; $("roomCode").textContent = j.room; setView("wait");
  } else if (j.status === "game"){
    if (j.waitAgain) $("oWait").textContent = "Raqib javobi kutilmoqda";
    if (j.same) return;
    const old = S;
    S = j.state; gid = S.gid; v = S.v; sel.clear();
    $("oWait").textContent = ""; $("err").textContent = "";
    events(old, S);
    setView("game"); render();
    animDeal = false; animThrow = false;
  }
}

function schedule(){
  clearTimeout(timer);
  let ms = 0;
  if (view === "wait") ms = 1500;
  else if (view === "game") ms = S && S.result ? 2500 : (S && S.actor === S.me ? 3000 : 1000);
  if (ms) timer = setTimeout(poll, ms);
}
async function poll(){
  if (busy){ schedule(); return; }
  const now = Date.now(), hb = now - lastHb > 5000;
  if (hb) lastHb = now;
  apply(await api("state", {gid, v, room, hb}));
  schedule();
}
async function act(path, extra){
  if (busy) return;
  clearTimeout(timer);
  apply(await api(path, extra));
  schedule();
}

/* ---------- kartalarni chizish ---------- */
const sv = (s, cls) => '<svg class="' + (cls||"") + '" viewBox="0 0 100 100"><use href="#s' + s + '"/></svg>';
function pips(r){
  const L = 35, R = 65, C = 50;
  if (r === 0) return [[L,24],[R,24],[L,50],[R,50],[L,76],[R,76]];
  if (r === 1) return [[L,24],[R,24],[L,50],[R,50],[L,76],[R,76],[C,37]];
  if (r === 2) return [[L,24],[R,24],[L,50],[R,50],[L,76],[R,76],[C,37],[C,63]];
  const four = [[L,20],[R,20],[L,40],[R,40],[L,60],[R,60],[L,80],[R,80]];
  if (r === 3) return [...four,[C,50]];
  return [...four,[C,30],[C,70]];            // 10
}
function cardEl(c){
  const s = suit(c), r = rank(c), label = RANKS[r];
  const el = document.createElement("div");
  el.className = "card " + (isRed(s) ? "red" : "blk");
  let h = '<div class="idx tl"><b>' + label + '</b>' + sv(s) + '</div><div class="idx br"><b>' + label + '</b>' + sv(s) + '</div><div class="field">';
  if (r === 8) h += '<span class="pip big" style="left:50%;top:50%">' + sv(s) + '</span>';
  else if (r >= 4 && r <= 6) h += '<div class="royal">' + sv(s) + '<b>' + label + '</b>' + sv(s) + '</div>';
  else pips(r).forEach(p => { h += '<span class="pip' + (p[1] > 50 ? " flip" : "") + '" style="left:' + p[0] + '%;top:' + p[1] + '%">' + sv(s) + '</span>'; });
  el.innerHTML = h + '</div>';
  return el;
}
function backEl(){ const d = document.createElement("div"); d.className = "card back"; return d; }
const tilt = c => ((c * 37) % 9 - 4);

function fillDots(el, n, limit){
  el.replaceChildren();
  for (let i = 0; i < limit; i++){ const d = document.createElement("i"); if (i < n) d.className = "on"; el.append(d); }
}

function validSel(){
  if (!S || S.result || S.actor !== S.me || !sel.size) return false;
  const cs = [...sel];
  if (S.phase === "attack") return new Set(cs.map(suit)).size === 1 && cs.length <= S.oppN;
  return cs.length === S.table.length;
}

function render(){
  if (!S) return;
  const mine = S.actor === S.me;
  $("oppName").textContent = S.opp;
  $("myScore").textContent = S.myScore;
  $("roundNo").textContent = "Raund " + S.round;
  fillDots($("myDots"), S.pen[0], S.limit);
  fillDots($("oppDots"), S.pen[1], S.limit);

  const oc = $("oppCards"); oc.replaceChildren();
  for (let i = 0; i < S.oppN; i++){
    const b = backEl(); if (animDeal){ b.classList.add("dealt"); b.style.setProperty("--i", i); } oc.append(b);
  }

  const dk = $("deck"); dk.replaceChildren();
  if (S.trumpCard !== null){
    const u = cardEl(S.trumpCard); u.classList.add("under"); dk.append(u);
    if (S.deckN > 1){ const b = backEl(); b.classList.add("stack"); if (S.deckN > 2) b.classList.add("two"); dk.append(b); }
    const n = document.createElement("div"); n.className = "deckn"; n.textContent = S.deckN + " ta karta"; dk.append(n);
  } else {
    const d = document.createElement("div"); d.className = "suitonly " + (isRed(S.trump) ? "red" : "blk");
    d.innerHTML = sv(S.trump); dk.append(d);
    const n = document.createElement("div"); n.className = "deckn"; n.textContent = "Kozir"; dk.append(n);
  }

  const tr = $("trick"); tr.replaceChildren(); tr.classList.remove("old");
  let shown = S.table, lastTxt = "", fresh = animThrow;
  if (!S.table.length && S.last){
    shown = S.last.att.concat(S.last.def); tr.classList.add("old");
    lastTxt = (S.last.winner === S.me ? "Yurishni siz oldingiz" : "Yurishni raqib oldi") + ", " + S.last.pts + " ochko";
  }
  const attackerIsMe = S.phase === "defend" && S.actor !== S.me;
  shown.forEach(c => {
    const e = cardEl(c); e.style.setProperty("--rot", tilt(c) + "deg");
    if (fresh){
      e.classList.add("fresh");
      e.style.setProperty("--fy", (S.table.length ? (attackerIsMe ? 110 : -110) : 0) + "px");
    }
    tr.append(e);
  });
  $("last").textContent = lastTxt;

  const hand = $("hand"); hand.replaceChildren(); hand.classList.toggle("locked", !mine || !!S.result);
  const cards = [...S.hand].sort((a, b) => suit(a) - suit(b) || rank(b) - rank(a));
  const n = cards.length;
  cards.forEach((c, i) => {
    const e = cardEl(c), off = i - (n - 1) / 2;
    e.style.setProperty("--r", (off * 3.2) + "deg");
    e.style.setProperty("--y", (Math.abs(off) * Math.abs(off) * 2) + "px");
    if (animDeal){ e.classList.add("dealt"); e.style.setProperty("--i", i); }
    if (sel.has(c)) e.classList.add("sel");
    e.onclick = () => { if (!mine || S.result) return; sel.has(c) ? sel.delete(c) : sel.add(c); sfx.tick(); render(); };
    hand.append(e);
  });

  let msg = "";
  if (!S.result){
    if (S.phase === "attack") msg = mine ? "Yurishingiz: bir mastdagi karta(lar)ni tanlang" : "Raqib yuryapti";
    else msg = mine ? "Raqib " + S.table.length + " ta karta tashladi, javob uchun " + S.table.length + " ta karta tanlang" : "Raqib javob beryapti";
  }
  $("msg").textContent = msg;
  $("play").disabled = !validSel();

  const r = S.result;
  if (r && Date.now() >= buraUntil){
    const m = r.match || {}, add = r.add || [0, 0];
    let title;
    if (m.over) title = m.winner === null ? "O'yin durang" : (m.winner === S.me ? "O'yinda yutdingiz" : "O'yinda yutqazdingiz");
    else title = r.winner === null ? "Raund durang" : (r.winner === S.me ? "Raundni yutdingiz" : "Raundni yutqazdingiz");
    $("oTitle").textContent = title;
    $("oWhy").textContent = r.why;
    $("oScore").textContent = (S.scores && !r.special) ? "Ochko: siz " + S.scores[S.me] + ", raqib " + S.scores[1 - S.me] : "";
    $("oPen").textContent = add[0] > 0 ? "Sizga +" + add[0] + " bal" : (add[1] > 0 ? "Raqibga +" + add[1] + " bal" : "Bal berilmadi");
    $("oTot").textContent = "Bal: siz " + S.pen[0] + ", raqib " + S.pen[1] + " (" + S.limit + " ga yetgan yutqazadi)";
    $("again").textContent = m.over ? "Yangi o'yin" : "Keyingi raund";
    $("again").disabled = false;
    $("over").hidden = false;
  } else $("over").hidden = true;
}

$("vsBot").onclick = () => act("bot");
$("create").onclick = () => { $("err").textContent = ""; act("create"); };
$("join").onclick = () => {
  const r = $("room").value.trim();
  if (!/^\d{4}$/.test(r)){ $("err").textContent = "Baza raqami 4 ta raqamdan iborat"; return; }
  $("err").textContent = ""; act("join", {room: r});
};
$("room").addEventListener("input", e => { e.target.value = e.target.value.replace(/\D/g, "").slice(0, 4); });
$("cancel").onclick = () => act("leave", {room});
$("play").onclick = () => { if (validSel()) act("play", {gid, cards: [...sel]}); };
$("leave").onclick = $("exit").onclick = () => act("leave", {gid, room});
$("again").onclick = () => { $("again").disabled = true; act("again", {gid}); };

/* lobbidagi bezak: yelpig'ichdek ochilgan 3 ta karta */
(function(){
  const hero = $("hero");
  [[8, -16], [15, 0], [25, 16]].forEach(p => {          // qarg'a tuzi, chillak qiroli, g'isht o'nligi
    const e = cardEl(p[0]);
    e.style.transform = "rotate(" + p[1] + "deg)";
    hero.append(e);
  });
})();

poll();   // sahifa yangilansa, davom etayotgan o'yinga qaytadi
</script>
</body>
</html>
'''
