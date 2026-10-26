from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import httpx
from django.conf import settings

from .risk import WeatherSample

logger = logging.getLogger(__name__)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
_CACHE: dict[tuple[float, float, str], tuple[float, WeatherSample]] = {}
CACHE_TTL_SECONDS = 900


class WeatherError(Exception):
    pass


def _to_utc_hour(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    else:
        moment = moment.astimezone(timezone.utc)
    return moment.replace(minute=0, second=0, microsecond=0)


def forecast_at(latitude: float, longitude: float, eta: datetime) -> WeatherSample:
    hour = _to_utc_hour(eta)
    key = (round(latitude, 3), round(longitude, 3), hour.isoformat())
    now = datetime.now(timezone.utc).timestamp()
    cached = _CACHE.get(key)
    if cached and now - cached[0] < CACHE_TTL_SECONDS:
        return cached[1]

    start = hour.date().isoformat()
    end = (hour + timedelta(hours=1)).date().isoformat()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,snowfall,wind_speed_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "UTC",
        "start_date": start,
        "end_date": end,
    }

    try:
        with httpx.Client(timeout=settings.HTTP_TIMEOUT_SECONDS, headers={"User-Agent": settings.USER_AGENT}) as client:
            response = client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as exc:
        raise WeatherError("Weather provider unavailable.") from exc

    hourly = data.get("hourly") or {}
    times = hourly.get("time") or []
    target = hour.strftime("%Y-%m-%dT%H:00")
    try:
        index = times.index(target)
    except ValueError:
        index = min(range(len(times)), key=lambda i: abs(_parse_hour(times[i]) - hour)) if times else None
    if index is None:
        raise WeatherError("No hourly forecast for checkpoint ETA.")

    # Open-Meteo snowfall is cm/hr; convert to inches/hr for PDF thresholds.
    snow_cm = float((hourly.get("snowfall") or [0])[index] or 0)
    sample = WeatherSample(
        wind_mph=round(float((hourly.get("wind_speed_10m") or [0])[index] or 0), 1),
        rain_in_hr=round(float((hourly.get("precipitation") or [0])[index] or 0), 3),
        snow_in_hr=round(snow_cm / 2.54, 3),
        temperature_f=round(float((hourly.get("temperature_2m") or [50])[index] or 50), 1),
    )
    _CACHE[key] = (now, sample)
    return sample


def _parse_hour(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def clear_weather_cache() -> None:
    _CACHE.clear()
