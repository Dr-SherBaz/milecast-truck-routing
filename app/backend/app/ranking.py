from __future__ import annotations

from .models import Route


def route_sort_key(route: Route) -> tuple[float, float, float, float]:
    summary = route.summary
    return (summary.severe_miles + summary.no_travel_miles, summary.high_miles, summary.average_risk, route.duration_minutes)


def rank_routes(routes: list[Route]) -> list[Route]:
    return sorted(routes, key=route_sort_key)
