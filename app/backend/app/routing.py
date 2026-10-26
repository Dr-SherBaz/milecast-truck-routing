from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class RouteDraft:
    id: str
    name: str
    distance_miles: float
    duration_minutes: float
    coordinates: list[tuple[float, float]]


class MockRoutingProvider:
    """Deterministic local provider; replaceable by an official routing adapter."""

    def get_alternatives(self, origin: str, destination: str) -> list[RouteDraft]:
        seed = int(hashlib.sha256(f"{origin}|{destination}".encode()).hexdigest()[:8], 16)
        base = 170 + seed % 160
        route_specs = [("north", 1.00, 1.00), ("central", 0.93, 0.94), ("south", 1.08, 1.06)]
        origin_point = _geocode_label(origin, seed, 0)
        destination_point = _geocode_label(destination, seed, 1)
        routes: list[RouteDraft] = []
        for index, (label, distance_factor, duration_factor) in enumerate(route_specs, start=1):
            distance = round(base * distance_factor, 1)
            duration = round((distance / 52) * 60 * duration_factor, 1)
            bend = (index - 2) * 0.055
            coords = [
                origin_point,
                (origin_point[0] + (destination_point[0] - origin_point[0]) * 0.33 + bend, origin_point[1] + (destination_point[1] - origin_point[1]) * 0.33 - bend),
                (origin_point[0] + (destination_point[0] - origin_point[0]) * 0.66 - bend, origin_point[1] + (destination_point[1] - origin_point[1]) * 0.66 + bend),
                destination_point,
            ]
            routes.append(RouteDraft(f"route-{index}", f"{label.title()} corridor", distance, duration, coords))
        return routes


def _geocode_label(label: str, seed: int, side: int) -> tuple[float, float]:
    value = int(hashlib.md5(label.lower().encode()).hexdigest()[:8], 16)
    latitude = 30.0 + ((value + seed + side * 7919) % 1500) / 100
    longitude = -122.0 + ((value // 17 + seed + side * 1231) % 2000) / 100
    return round(latitude, 5), round(longitude, 5)


def interpolate_coordinates(coords: list[tuple[float, float]], fraction: float) -> tuple[float, float]:
    fraction = min(max(fraction, 0), 1)
    segments = [_distance(a, b) for a, b in zip(coords, coords[1:])]
    target = sum(segments) * fraction
    travelled = 0.0
    for (start, end), segment in zip(zip(coords, coords[1:]), segments):
        if travelled + segment >= target:
            local = (target - travelled) / segment if segment else 0
            return start[0] + (end[0] - start[0]) * local, start[1] + (end[1] - start[1]) * local
        travelled += segment
    return coords[-1]


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])
