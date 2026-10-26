# Milecast — Weather-Aware Truck Routing

Independent Spotter full-stack assessment build: **React (Next.js) + Django REST**.

Drivers enter origin, destination, departure time, and load weight. The app builds **three** corridor alternatives, samples weather every **10 / 25 / 50** miles at each checkpoint ETA, applies the PDF wind/rain/snow and load rules, recommends a route (severe → high → average risk → time), and shows a **corridor weather heatmap** with a live **0–48 hour** forecast slider.

## Why this stack

The brief asks for React + Django. This implementation uses Django + DRF for the API and Next.js for the React UI. Routing/geocoding/weather use public providers (no routing engine built in-house).

## Workspace

| Path | Role |
|------|------|
| `fs-assessment-spotter.pdf` | Source brief |
| `app/backend/` | Django API (submission) |
| `app/frontend/` | Next.js UI (submission) |
| `reference/` | Supplied repos kept for comparison only |

Brand: **Milecast** — unique UI and service layout, not a copy of the reference apps.

## Quick start

Terminal 1 — API:

```powershell
cd app/backend
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver 8000
```

Terminal 2 — UI:

```powershell
cd app/frontend
npm install
npm run dev
```

Open http://localhost:3000

Optional: set `ORS_API_KEY` in `app/backend/.env` for OpenRouteService HGV routing. Without it, the API uses OSRM and guarantees three alternatives.

## Providers

- Geocoding: Nominatim
- Routing: OpenRouteService (optional key) or OSRM
- Weather: Open-Meteo hourly at checkpoint ETA

## Validation

```powershell
cd app/backend
python -m pytest

cd ../frontend
npm run build
```

## Deliverables

See `DELIVERABLES.md` for the live links.

- GitHub: https://github.com/Dr-SherBaz/milecast-truck-routing
- Hosted demo (Cloudflare tunnel while local servers run): see `DELIVERABLES.md`
- Voiceover-ready walkthrough video: `walkthrough/Milecast-Walkthrough-VOICEOVER-READY.mp4` + `walkthrough/VOICEOVER_SCRIPT.md`

## Design notes

- Risk thresholds and load overrides match the PDF exactly
- No-travel miles outrank severe miles when sorting
- Forecast slider re-queries the API so the corridor heatmap updates live
