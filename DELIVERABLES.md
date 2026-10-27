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

## 3. Loom walkthrough — done

**Loom (submission link):**  
https://www.loom.com/share/aa883cfe822f45c0be7f98c62dc52e5c

Local source cut (optional):  
`walkthrough/Milecast-Interactive-Walkthrough.mp4`

Timed voiceover script used for the recording:  
`walkthrough/VOICEOVER_SCRIPT.md`
