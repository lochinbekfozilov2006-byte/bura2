# Bura

Ikki kishilik karta o'yini (botga qarshi va onlayn, 4 xonali baza raqami bilan).

## Vercel'ga joylash

1. Bu papkadagi hamma fayllarni GitHub repo ildiziga yuklang:
   `main.py`, `page.py`, `requirements.txt`.
2. Vercel -> New Project -> shu repo. Preset: Python (yoki Flask), boshqa sozlama kerak emas. Deploy.
3. Vercel loyihasida Storage bo'limiga kiring, Upstash Redis (bepul tarif) qo'shing va loyihaga ulang.
   U `KV_REST_API_URL` va `KV_REST_API_TOKEN` o'zgaruvchilarini o'zi qo'shadi.
4. Settings -> Environment Variables: `ADMIN_CODE` = o'zingiz o'ylagan maxfiy so'z.
5. Redeploy qiling (o'zgaruvchilar yangi deploy'dan keyin kuchga kiradi).

## Kompyuterda sinash

    pip install flask
    python main.py

Brauzerda http://localhost:8080 (Redis shart emas, holat xotirada saqlanadi).
