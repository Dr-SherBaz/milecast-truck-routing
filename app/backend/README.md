# Milecast API (Django)

Django + Django REST Framework backend for the Spotter weather-aware truck routing assessment.

## Endpoints

- `GET /health`
- `POST /api/plan`

## Providers

- Geocoding: OpenStreetMap Nominatim
- Routing: OpenRouteService HGV when `ORS_API_KEY` is set, otherwise OSRM public with detour padding to guarantee three alternatives
- Weather: Open-Meteo hourly forecast at each checkpoint ETA

## Run

```powershell
cd app/backend
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver 8000
```

## Tests

```powershell
python -m pytest
```
