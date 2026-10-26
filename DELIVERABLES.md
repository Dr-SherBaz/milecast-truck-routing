# Assessment deliverables

## 1. GitHub repository — done

Public repo: https://github.com/Dr-SherBaz/milecast-truck-routing

## 2. Hosted application — live demo tunnel

While this machine keeps the local servers running:

**App URL:** https://varying-centuries-allow-edmonton.trycloudflare.com

That URL proxies the Next.js UI; `/api/plan` is rewritten to the local Django API.

To restart the hosted demo later:

```powershell
cd app\backend
python manage.py runserver 0.0.0.0:8000

cd ..\frontend
npm run dev -- -H 0.0.0.0 -p 3000

..\..\tools\cloudflared.exe tunnel --url http://127.0.0.1:3000
```

For a permanent host (Render/Vercel/Railway), use `docker-compose.yml` or deploy API + web separately and set `CORS_ALLOWED_ORIGINS` / `NEXT_PUBLIC_API_URL`.

## 3. Walkthrough video — voiceover-ready

Silent demo MP4 (import and narrate):

`walkthrough/Milecast-Walkthrough-VOICEOVER-READY.mp4`

Script with timestamps:

`walkthrough/VOICEOVER_SCRIPT.md`

Record your voice in CapCut / Descript / Loom over that file (or do a live Loom using the hosted URL and the script).
