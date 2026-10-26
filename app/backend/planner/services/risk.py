from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"
    NO_TRAVEL = "no_travel"


LEVEL_SCORE = {
    RiskLevel.LOW: 0.0,
    RiskLevel.MODERATE: 1.0,
    RiskLevel.HIGH: 2.0,
    RiskLevel.SEVERE: 3.0,
    RiskLevel.NO_TRAVEL: 4.0,
}


@dataclass(frozen=True)
class WeatherSample:
    wind_mph: float
    rain_in_hr: float
    snow_in_hr: float
    temperature_f: float


@dataclass(frozen=True)
class RiskResult:
    level: RiskLevel
    score: float
    reasons: list[str]


def wind_level(wind_mph: float) -> RiskLevel:
    if wind_mph < 25:
        return RiskLevel.LOW
    if wind_mph < 35:
        return RiskLevel.MODERATE
    if wind_mph < 45:
        return RiskLevel.HIGH
    if wind_mph < 55:
        return RiskLevel.SEVERE
    return RiskLevel.NO_TRAVEL


def rain_level(rain_in_hr: float) -> RiskLevel:
    if rain_in_hr < 0.10:
        return RiskLevel.LOW
    if rain_in_hr < 0.25:
        return RiskLevel.MODERATE
    if rain_in_hr < 0.50:
        return RiskLevel.HIGH
    if rain_in_hr <= 1.00:
        return RiskLevel.SEVERE
    return RiskLevel.NO_TRAVEL


def snow_level(snow_in_hr: float) -> RiskLevel:
    if snow_in_hr < 0.5:
        return RiskLevel.LOW
    if snow_in_hr < 1.0:
        return RiskLevel.MODERATE
    if snow_in_hr < 2.0:
        return RiskLevel.HIGH
    if snow_in_hr <= 3.0:
        return RiskLevel.SEVERE
    return RiskLevel.NO_TRAVEL


def classify_weather(weather: WeatherSample, load_weight_lb: int) -> RiskResult:
    """Apply PDF wind/rain/snow thresholds, then load overrides."""
    components = [
        ("Wind", wind_level(weather.wind_mph)),
        ("Rain", rain_level(weather.rain_in_hr)),
        ("Snow", snow_level(weather.snow_in_hr)),
    ]
    reasons = [name for name, level in components if level != RiskLevel.LOW]
    levels = [level for _, level in components]

    if weather.wind_mph >= 55:
        levels.append(RiskLevel.NO_TRAVEL)
        reasons.append("Wind ≥ 55 mph — no travel for any load")
    elif 45 <= weather.wind_mph < 55 and load_weight_lb > 30_000:
        levels.append(RiskLevel.NO_TRAVEL)
        reasons.append("45–54 mph wind with load > 30,000 lb — no travel")
    elif 35 <= weather.wind_mph < 45 and load_weight_lb > 40_000:
        levels.append(RiskLevel.SEVERE)
        reasons.append("35–44 mph wind with load > 40,000 lb — severe")

    level = max(levels, key=lambda item: LEVEL_SCORE[item])
    return RiskResult(
        level=level,
        score=LEVEL_SCORE[level],
        reasons=reasons or ["Conditions within low-risk thresholds"],
    )


def summarize_risk_miles(segments: list[tuple[RiskLevel, float]]) -> dict[str, float]:
    totals = {level: 0.0 for level in RiskLevel}
    weighted = 0.0
    distance = 0.0
    for level, miles in segments:
        totals[level] += miles
        weighted += LEVEL_SCORE[level] * miles
        distance += miles
    return {
        "low_miles": round(totals[RiskLevel.LOW], 2),
        "moderate_miles": round(totals[RiskLevel.MODERATE], 2),
        "high_miles": round(totals[RiskLevel.HIGH], 2),
        "severe_miles": round(totals[RiskLevel.SEVERE], 2),
        "no_travel_miles": round(totals[RiskLevel.NO_TRAVEL], 2),
        "average_risk": round(weighted / distance, 3) if distance else 0.0,
    }
