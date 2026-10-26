from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.models import WeatherPoint
from app.risk import classify_weather
from app.models import RiskLevel

client = TestClient(app)


def weather(wind=10, rain=0, snow=0):
    return WeatherPoint(wind_mph=wind, rain_in_hr=rain, snow_in_hr=snow, temperature_f=50)


def test_exact_thresholds():
    assert classify_weather(weather(wind=24.9), 10_000).level == RiskLevel.low
    assert classify_weather(weather(wind=25), 10_000).level == RiskLevel.moderate
    assert classify_weather(weather(wind=35), 10_000).level == RiskLevel.high
    assert classify_weather(weather(wind=45), 10_000).level == RiskLevel.severe
    assert classify_weather(weather(wind=55), 10_000).level == RiskLevel.no_travel
    assert classify_weather(weather(rain=1.01), 10_000).level == RiskLevel.no_travel
    assert classify_weather(weather(snow=3.01), 10_000).level == RiskLevel.no_travel


def test_load_overrides():
    assert classify_weather(weather(wind=50), 30_001).level == RiskLevel.no_travel
    assert classify_weather(weather(wind=40), 40_001).level == RiskLevel.severe


def test_plan_returns_exactly_three_routes_and_interval():
    response = client.post("/api/plan", json={"origin": "Denver, CO", "destination": "Chicago, IL", "departure_time": datetime.now(timezone.utc).isoformat(), "load_weight_lb": 25_000, "checkpoint_interval_miles": 50})
    assert response.status_code == 200
    body = response.json()
    assert len(body["routes"]) == 3
    assert all(point["forecast_offset_hours"] == 0 for route in body["routes"] for point in route["checkpoints"])
    assert body["forecast_window_hours"] == 48


def test_forecast_offset_validation():
    payload = {"origin": "A", "destination": "B", "departure_time": datetime.now(timezone.utc).isoformat(), "load_weight_lb": 1, "forecast_offset_hours": 49}
    assert client.post("/api/plan", json=payload).status_code == 422


def test_invalid_interval_validation():
    payload = {"origin": "A", "destination": "B", "departure_time": datetime.now(timezone.utc).isoformat(), "load_weight_lb": 1, "checkpoint_interval_miles": 15}
    assert client.post("/api/plan", json=payload).status_code == 422
