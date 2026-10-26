# Milecast UI

Next.js / React client for the Spotter weather-aware truck routing assessment.

## Features

- Origin, destination, departure time, load weight
- Checkpoint spacing 10 / 25 / 50 miles
- Live 0–48 hour forecast slider that re-plans the corridor
- Leaflet map with risk-colored corridor heatmap segments
- Route cards with severe / high / no-travel miles and checkpoint ETAs

## Run

```powershell
cd app/frontend
npm install
npm run dev
```

Open http://localhost:3000 with the Django API on port 8000.
