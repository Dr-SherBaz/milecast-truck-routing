# Weather-Aware Truck Routing Assessment

This is an independent implementation of the supplied assessment brief. The two supplied GitHub repositories are preserved under `reference/` for comparison only; the application under `app/` was built separately and does not copy their implementation.

## What the assessment asks for

The PDF requires a React + Django-style full-stack application that accepts origin, destination, departure date/time, and load weight; creates exactly three route alternatives; samples weather every 10, 25, or 50 miles at the truck's ETA; applies wind/rain/snow and load rules; ranks routes by severe miles, high-risk miles, average risk, then travel time; and presents routes, checkpoints, summaries, a map, and a 0–48 hour forecast heatmap slider.

## Workspace

- `fs-assessment-spotter.pdf` — source brief
- `fs-assessment-spotter.txt` — extracted text used during implementation
- `reference/` — supplied repositories, isolated and read-only
- `app/backend/` — independent FastAPI service
- `app/frontend/` — independent Next.js/React client

The PDF says Django, while this implementation uses FastAPI for a smaller typed API boundary. This is an implementation choice, not copied code; the behavior and deliverables remain aligned with the brief.

## Run locally

Start the API:

```powershell
cd app/backend
C:\Users\Sher\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt
C:\Users\Sher\AppData\Local\Programs\Python\Python312\python.exe -m uvicorn app.main:app --reload
```

Start the UI in another terminal:

```powershell
cd app/frontend
npm install
npm run dev
```

Open `http://localhost:3000`. No API credentials are required: deterministic mock routing and weather providers are enabled by default. Production adapters should use official providers and environment variables documented in `.env.example` files; secrets are never committed.

## Validation

Backend tests are in `app/backend/tests/` and cover threshold boundaries, load overrides, exact route count, checkpoint interval behavior, and forecast validation. Frontend production validation is `npm run build`; lint is `npm run lint`.

## Deliberate limitations

The local provider mode uses deterministic synthetic coordinates and weather, so it demonstrates the complete product flow but is not a live dispatch system. Before hosting, connect official geocoding/routing/weather services, add rate limits and observability, and verify road restrictions with authoritative advisories. GitHub publishing, hosting, and the Loom walkthrough remain separate deployment steps requiring explicit approval.
