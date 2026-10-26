# Routewise frontend

Independent Next.js/React UI for the weather-aware truck-routing assessment.

## Run

```powershell
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_URL` in `.env.local` when the API is not running at `http://localhost:8000`.

The interface works with the backend's deterministic mock providers. It renders three route alternatives, checkpoint risk, ETA-aware weather, route recommendation, a Leaflet map, a corridor heatmap, and an explicit 0–48 hour forecast slider.
