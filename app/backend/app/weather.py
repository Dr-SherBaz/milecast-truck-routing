from __future__ import annotations

import hashlib
from datetime import datetime

from .models import WeatherPoint


class MockWeatherProvider:
    """Deterministic weather corridor used when no external weather key is configured."""

    def forecast(self, latitude: float, longitude: float, eta: datetime) -> WeatherPoint:
        key = f"{latitude:.3f}|{longitude:.3f}|{eta.hour}|{eta.day}"
        seed = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)
        return WeatherPoint(
            wind_mph=round(18 + seed % 43 + (eta.hour % 7) * 0.7, 1),
            rain_in_hr=round((seed % 90) / 100, 2),
            snow_in_hr=round(((seed // 11) % 35) / 10, 2) if eta.month in {11, 12, 1, 2, 3} else 0,
            temperature_f=round(28 + ((seed // 17) % 55), 1),
        )
