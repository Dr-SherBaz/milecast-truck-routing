# Assessment deliverables checklist

## 1. GitHub repository

```powershell
cd C:\Users\Sher_\Desktop\spotter-truck-routing-assessment
git add app README.md DELIVERABLES.md docker-compose.yml .gitignore
git status
# After you approve a commit message, create the commit, then:
# gh repo create milecast-truck-routing --private --source=. --remote=origin --push
```

## 2. Hosted application

Option A — Docker:

```powershell
docker compose up --build
```

Option B — Managed hosts:

- API: Railway / Render / Fly — run `gunicorn config.wsgi:application`
- UI: Vercel — set `NEXT_PUBLIC_API_URL` to the public API URL and allow that origin in `CORS_ALLOWED_ORIGINS`

## 3. Loom walkthrough (5–10 min)

Suggested script:

1. Show the PDF requirements briefly
2. Enter origin / destination / departure / load weight
3. Build plan — point out three corridors on the map
4. Open checkpoint details and risk badges
5. Drag the 0–48h forecast slider and show heatmap refresh
6. Explain recommendation order (severe → high → average risk → time)
7. Mention Django API + Nominatim / OSRM|ORS / Open-Meteo
