from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone

from .geocoding import geocode_place
from .ranking import rank_routes, recommendation_reason
from .risk import RiskLevel, classify_weather, summarize_risk_miles
from .routing import RouteDraft, get_three_routes, interpolate_coordinates
from .weather import forecast_at


ALLOWED_INTERVALS = {10, 25, 50}


def build_plan(
    *,
    origin: str,
    destination: str,
    departure_time: datetime,
    load_weight_lb: int,
    checkpoint_interval_miles: int,
    forecast_offset_hours: int,
) -> dict:
    if checkpoint_interval_miles not in ALLOWED_INTERVALS:
        raise ValueError("checkpoint_interval_miles must be 10, 25, or 50")
    if not 0 <= forecast_offset_hours <= 48:
        raise ValueError("forecast_offset_hours must be between 0 and 48")
    if load_weight_lb <= 0 or load_weight_lb > 100_000:
        raise ValueError("load_weight_lb must be between 1 and 100000")

    if departure_time.tzinfo is None:
        departure_time = departure_time.replace(tzinfo=timezone.utc)

    origin_point = geocode_place(origin)
    destination_point = geocode_place(destination)
    drafts = get_three_routes(origin_point, destination_point)
    if len(drafts) != 3:
        raise RuntimeError("Planner must produce exactly three route alternatives")

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [
            pool.submit(
                _enrich_route,
                draft=draft,
                departure=departure_time,
                interval=checkpoint_interval_miles,
                load_weight_lb=load_weight_lb,
                forecast_offset_hours=forecast_offset_hours,
            )
            for draft in drafts
        ]
        routes = [future.result() for future in futures]

    ranked = rank_routes(routes)
    recommended = ranked[0]
    heatmap = []
    for route in ranked:
        heatmap.extend(route["checkpoints"])

    return {
        "request": {
            "origin": origin,
            "destination": destination,
            "departure_time": departure_time.isoformat(),
            "load_weight_lb": load_weight_lb,
            "checkpoint_interval_miles": checkpoint_interval_miles,
            "forecast_offset_hours": forecast_offset_hours,
            "resolved_origin": origin_point.label,
            "resolved_destination": destination_point.label,
        },
        "routes": routes,
        "recommended_route_id": recommended["id"],
        "recommendation_reason": recommendation_reason(recommended),
        "corridor_heatmap": heatmap,
        "forecast_window_hours": 48,
        "provider_mode": "live",
    }


def _enrich_route(
    *,
    draft: RouteDraft,
    departure: datetime,
    interval: int,
    load_weight_lb: int,
    forecast_offset_hours: int,
) -> dict:
    miles = list(range(interval, int(draft.distance_miles), interval))
    if not miles or miles[-1] != round(draft.distance_miles):
        miles.append(round(draft.distance_miles, 1))

    pending: list[tuple[float, float, float, datetime]] = []
    for mile in miles:
        fraction = min(mile / draft.distance_miles, 1.0) if draft.distance_miles else 1.0
        eta = departure + timedelta(minutes=draft.duration_minutes * fraction) + timedelta(hours=forecast_offset_hours)
        lat, lon = interpolate_coordinates(draft.coordinates, fraction)
        pending.append((mile, lat, lon, eta))

    weather_by_index: dict[int, object] = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        future_map = {
            pool.submit(forecast_at, lat, lon, eta): index
            for index, (_mile, lat, lon, eta) in enumerate(pending)
        }
        for future in as_completed(future_map):
            weather_by_index[future_map[future]] = future.result()

    checkpoints = []
    for index, (mile, lat, lon, eta) in enumerate(pending):
        weather = weather_by_index[index]
        risk = classify_weather(weather, load_weight_lb)
        checkpoints.append(
            {
                "mile": mile,
                "latitude": round(lat, 5),
                "longitude": round(lon, 5),
                "eta": eta.isoformat(),
                "forecast_offset_hours": forecast_offset_hours,
                "weather": {
                    "wind_mph": weather.wind_mph,
                    "rain_in_hr": weather.rain_in_hr,
                    "snow_in_hr": weather.snow_in_hr,
                    "temperature_f": weather.temperature_f,
                },
                "risk_level": risk.level.value,
                "risk_score": risk.score,
                "risk_reasons": risk.reasons,
            }
        )

    segments: list[tuple[RiskLevel, float]] = []
    for index, point in enumerate(checkpoints):
        previous = checkpoints[index - 1]["mile"] if index else 0.0
        if index < len(checkpoints) - 1:
            span = max(point["mile"] - previous, 0.1)
        else:
            span = max(draft.distance_miles - previous, 0.1)
        segments.append((RiskLevel(point["risk_level"]), span))

    return {
        "id": draft.id,
        "name": draft.name,
        "distance_miles": draft.distance_miles,
        "duration_minutes": draft.duration_minutes,
        "coordinates": draft.coordinates,
        "checkpoints": checkpoints,
        "summary": summarize_risk_miles(segments),
    }
