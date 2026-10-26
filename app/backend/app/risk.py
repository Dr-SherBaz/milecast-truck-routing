from __future__ import annotations

from dataclasses import dataclass

from .models import RiskLevel, RouteSummary, WeatherPoint


@dataclass(frozen=True)
class RiskResult:
    level: RiskLevel
    score: float
    reasons: list[str]


def _wind_level(wind: float) -> RiskLevel:
    if wind < 25:
        return RiskLevel.low
    if wind < 35:
        return RiskLevel.moderate
    if wind < 45:
        return RiskLevel.high
    if wind < 55:
        return RiskLevel.severe
    return RiskLevel.no_travel


def _rain_level(rain: float) -> RiskLevel:
    if rain < 0.10:
        return RiskLevel.low
    if rain < 0.25:
        return RiskLevel.moderate
    if rain < 0.50:
        return RiskLevel.high
    if rain <= 1.00:
        return RiskLevel.severe
    return RiskLevel.no_travel


def _snow_level(snow: float) -> RiskLevel:
    if snow < 0.5:
        return RiskLevel.low
    if snow < 1.0:
        return RiskLevel.moderate
    if snow < 2.0:
        return RiskLevel.high
    if snow <= 3.0:
        return RiskLevel.severe
    return RiskLevel.no_travel


_LEVEL_SCORE = {
    RiskLevel.low: 0.0,
    RiskLevel.moderate: 1.0,
    RiskLevel.high: 2.0,
    RiskLevel.severe: 3.0,
    RiskLevel.no_travel: 4.0,
}


def classify_weather(weather: WeatherPoint, load_weight_lb: int) -> RiskResult:
    component_levels = [
        ("wind", _wind_level(weather.wind_mph)),
        ("rain", _rain_level(weather.rain_in_hr)),
        ("snow", _snow_level(weather.snow_in_hr)),
    ]
    reasons = [name.replace("_", " ").title() for name, level in component_levels if level != RiskLevel.low]
    levels = [level for _, level in component_levels]

    if weather.wind_mph >= 55:
        levels.append(RiskLevel.no_travel)
        reasons.append("Wind is at or above 55 mph")
    elif 45 <= weather.wind_mph < 55 and load_weight_lb > 30_000:
        levels.append(RiskLevel.no_travel)
        reasons.append("Heavy load exceeds 30,000 lb in 45–54 mph wind")
    elif 35 <= weather.wind_mph < 45 and load_weight_lb > 40_000:
        levels.append(RiskLevel.severe)
        reasons.append("Heavy load exceeds 40,000 lb in 35–44 mph wind")

    level = max(levels, key=lambda item: _LEVEL_SCORE[item])
    score = _LEVEL_SCORE[level]
    return RiskResult(level=level, score=score, reasons=reasons or ["Conditions are within low-risk thresholds"])


def summarize_risks(level_miles: list[tuple[RiskLevel, float]]) -> RouteSummary:
    totals = {level: 0.0 for level in RiskLevel}
    weighted_score = 0.0
    total = 0.0
    for level, miles in level_miles:
        totals[level] += miles
        weighted_score += _LEVEL_SCORE[level] * miles
        total += miles
    return RouteSummary(
        low_miles=totals[RiskLevel.low],
        moderate_miles=totals[RiskLevel.moderate],
        high_miles=totals[RiskLevel.high],
        severe_miles=totals[RiskLevel.severe],
        no_travel_miles=totals[RiskLevel.no_travel],
        average_risk=weighted_score / total if total else 0,
    )
