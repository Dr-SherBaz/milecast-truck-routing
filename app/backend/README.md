# Routing API

Independent FastAPI implementation for the assessment. It uses deterministic mock routing and weather providers by default so local development and tests do not require credentials. Provider interfaces can be replaced with official routing/geocoding/weather adapters without changing the planning contract.

## Run

```powershell
C:\Users\Sher\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt
C:\Users\Sher\AppData\Local\Programs\Python\Python312\python.exe -m uvicorn app.main:app --reload
```

Endpoint: `POST /api/plan`. The request accepts `origin`, `destination`, ISO `departure_time`, `load_weight_lb`, `checkpoint_interval_miles` (10, 25, or 50), and `forecast_offset_hours` (0–48).
