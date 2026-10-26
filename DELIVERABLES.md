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

## 3. Walkthrough video — interactive + voiceover

**Main recording (use this):**  
`walkthrough/Milecast-Interactive-Walkthrough.mp4`

- Visible custom cursor with human-style moves (slow / fast / circles / wobble)
- Types inputs, points at risk rules, **drags the 0–48h slider**, builds plan
- Traces the corridor heatmap, hovers route cards, opens checkpoint details
- Second slider nudge to show live refresh

**Script (casual English + pauses):**  
`walkthrough/VOICEOVER_SCRIPT.md`

Import the MP4 into CapCut / Descript / Loom and narrate over it.

Older static title-card cut (optional B-roll):  
`walkthrough/Milecast-Walkthrough-VOICEOVER-READY.mp4`
