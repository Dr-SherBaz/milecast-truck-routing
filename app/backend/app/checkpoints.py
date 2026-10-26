from __future__ import annotations

from datetime import datetime, timedelta

from .models import Checkpoint, RiskLevel
from .risk import classify_weather
from .routing import RouteDraft, interpolate_coordinates
from .weather import MockWeatherProvider


def build_checkpoints(route: RouteDraft, departure: datetime, interval: int, load_weight_lb: int, forecast_offset_hours: int, weather_provider: MockWeatherProvider) -> list[Checkpoint]:
    miles = list(range(interval, int(route.distance_miles), interval))
    if not miles or miles[-1] != round(route.distance_miles):
        miles.append(round(route.distance_miles, 1))
    checkpoints: list[Checkpoint] = []
    for mile in miles:
        fraction = mile / route.distance_miles
        eta = departure + timedelta(minutes=route.duration_minutes * fraction) + timedelta(hours=forecast_offset_hours)
        latitude, longitude = interpolate_coordinates(route.coordinates, fraction)
        weather = weather_provider.forecast(latitude, longitude, eta)
        risk = classify_weather(weather, load_weight_lb)
        checkpoints.append(Checkpoint(mile=mile, latitude=latitude, longitude=longitude, eta=eta, forecast_offset_hours=forecast_offset_hours, weather=weather, risk_level=risk.level, risk_score=risk.score, risk_reasons=risk.reasons))
    return checkpoints


def checkpoint_miles(distance: float, interval: int) -> list[float]:
    values = list(range(interval, int(distance), interval))
    if not values or values[-1] != distance:
        values.append(round(distance, 1))
    return values
