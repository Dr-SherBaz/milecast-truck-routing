from __future__ import annotations

from typing import Any


def route_sort_key(route: dict[str, Any]) -> tuple[float, float, float, float, float]:
    """PDF preference: fewest severe, fewest high, lowest average risk, shortest time.

    No-travel miles are ranked first because they are worse than severe.
    """
    summary = route["summary"]
    return (
        summary["no_travel_miles"],
        summary["severe_miles"],
        summary["high_miles"],
        summary["average_risk"],
        route["duration_minutes"],
    )


def rank_routes(routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(routes, key=route_sort_key)


def recommendation_reason(route: dict[str, Any]) -> str:
    summary = route["summary"]
    if summary["no_travel_miles"] > 0:
        return (
            f"{route['name']} ranks best on the PDF criteria, but still includes "
            f"{summary['no_travel_miles']:.0f} no-travel miles — verify advisories before departure."
        )
    return (
        f"{route['name']} is recommended: fewest severe miles, then high miles, "
        "average risk, and travel time."
    )
