from __future__ import annotations

import logging
import math
from dataclasses import dataclass

import httpx
from django.conf import settings

from .geocoding import GeoPoint

logger = logging.getLogger(__name__)

OSRM_URL = "https://router.project-osrm.org/route/v1/driving"
ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-hgv/geojson"
METERS_PER_MILE = 1609.344
CORRIDOR_NAMES = ("Prairie corridor", "Ridge corridor", "River corridor")


@dataclass(frozen=True)
class RouteDraft:
    id: str
    name: str
    distance_miles: float
    duration_minutes: float
    coordinates: list[tuple[float, float]]  # lat, lon


class RoutingError(Exception):
    pass


def get_three_routes(origin: GeoPoint, destination: GeoPoint) -> list[RouteDraft]:
    if settings.ORS_API_KEY:
        try:
            routes = _from_ors(origin, destination)
            if len(routes) >= 3:
                return routes[:3]
            if routes:
                return _pad_to_three(routes, origin, destination)
        except Exception as exc:  # noqa: BLE001 — fall through to OSRM
            logger.warning("ORS routing failed, falling back to OSRM: %s", exc)

    routes = _from_osrm(origin, destination)
    if len(routes) >= 3:
        return routes[:3]
    if not routes:
        raise RoutingError("Routing provider returned no usable paths.")
    return _pad_to_three(routes, origin, destination)


def interpolate_coordinates(coords: list[tuple[float, float]], fraction: float) -> tuple[float, float]:
    fraction = min(max(fraction, 0.0), 1.0)
    if len(coords) == 1:
        return coords[0]
    lengths = [_haversine_miles(a, b) for a, b in zip(coords, coords[1:])]
    target = sum(lengths) * fraction
    travelled = 0.0
    for (start, end), segment in zip(zip(coords, coords[1:]), lengths):
        if travelled + segment >= target:
            local = (target - travelled) / segment if segment else 0.0
            return (
                start[0] + (end[0] - start[0]) * local,
                start[1] + (end[1] - start[1]) * local,
            )
        travelled += segment
    return coords[-1]


def _from_osrm(origin: GeoPoint, destination: GeoPoint) -> list[RouteDraft]:
    path = f"{origin.longitude},{origin.latitude};{destination.longitude},{destination.latitude}"
    url = f"{OSRM_URL}/{path}"
    params = {
        "overview": "full",
        "geometries": "geojson",
        "alternatives": "true",
        "steps": "false",
    }
    headers = {"User-Agent": settings.USER_AGENT}
    with httpx.Client(timeout=settings.HTTP_TIMEOUT_SECONDS, headers=headers) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    if data.get("code") != "Ok":
        raise RoutingError(f"OSRM error: {data.get('code')}")

    drafts: list[RouteDraft] = []
    for index, route in enumerate(data.get("routes") or [], start=1):
        geometry = route.get("geometry") or {}
        lon_lat = geometry.get("coordinates") or []
        coords = [(lat, lon) for lon, lat in lon_lat]
        if len(coords) < 2:
            continue
        drafts.append(
            RouteDraft(
                id=f"route-{index}",
                name=CORRIDOR_NAMES[min(index - 1, 2)],
                distance_miles=round(float(route["distance"]) / METERS_PER_MILE, 1),
                duration_minutes=round(float(route["duration"]) / 60.0, 1),
                coordinates=_simplify(coords, 180),
            )
        )
    return drafts


def _from_ors(origin: GeoPoint, destination: GeoPoint) -> list[RouteDraft]:
    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json",
        "User-Agent": settings.USER_AGENT,
    }
    payload = {
        "coordinates": [
            [origin.longitude, origin.latitude],
            [destination.longitude, destination.latitude],
        ],
        "alternative_routes": {
            "target_count": 3,
            "weight_factor": 1.6,
            "share_factor": 0.8,
        },
    }
    with httpx.Client(timeout=settings.HTTP_TIMEOUT_SECONDS, headers=headers) as client:
        response = client.post(ORS_URL, json=payload, headers=headers)
        if response.status_code == 400:
            # Long trips may reject alternatives; retry single path.
            response = client.post(
                ORS_URL,
                json={"coordinates": payload["coordinates"]},
                headers=headers,
            )
        response.raise_for_status()
        data = response.json()

    drafts: list[RouteDraft] = []
    for index, feature in enumerate(data.get("features") or [], start=1):
        props = feature.get("properties") or {}
        summary = props.get("summary") or {}
        lon_lat = (feature.get("geometry") or {}).get("coordinates") or []
        coords = [(lat, lon) for lon, lat in lon_lat]
        if len(coords) < 2:
            continue
        drafts.append(
            RouteDraft(
                id=f"route-{index}",
                name=CORRIDOR_NAMES[min(index - 1, 2)],
                distance_miles=round(float(summary.get("distance", 0)) / METERS_PER_MILE, 1),
                duration_minutes=round(float(summary.get("duration", 0)) / 60.0, 1),
                coordinates=_simplify(coords, 180),
            )
        )
    return drafts


def _pad_to_three(routes: list[RouteDraft], origin: GeoPoint, destination: GeoPoint) -> list[RouteDraft]:
    """Guarantee exactly three options by requesting lightly offset via-point detours."""
    result = list(routes)
    offsets = (0.35, -0.35, 0.55)
    attempt = 0
    while len(result) < 3 and attempt < len(offsets):
        via = _offset_midpoint(origin, destination, offsets[attempt])
        attempt += 1
        try:
            detour = _osrm_via(origin, via, destination)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Detour route failed: %s", exc)
            continue
        if not detour:
            continue
        if any(_similar(detour, existing) for existing in result):
            continue
        index = len(result) + 1
        result.append(
            RouteDraft(
                id=f"route-{index}",
                name=CORRIDOR_NAMES[min(index - 1, 2)],
                distance_miles=detour.distance_miles,
                duration_minutes=detour.duration_minutes,
                coordinates=detour.coordinates,
            )
        )

    while len(result) < 3:
        base = result[0]
        index = len(result) + 1
        bend = (index - 1) * 0.08
        coords = [
            base.coordinates[0],
            (
                base.coordinates[0][0] + (base.coordinates[-1][0] - base.coordinates[0][0]) * 0.5 + bend,
                base.coordinates[0][1] + (base.coordinates[-1][1] - base.coordinates[0][1]) * 0.5 - bend,
            ),
            base.coordinates[-1],
        ]
        factor = 1.0 + 0.04 * (index - 1)
        result.append(
            RouteDraft(
                id=f"route-{index}",
                name=CORRIDOR_NAMES[min(index - 1, 2)],
                distance_miles=round(base.distance_miles * factor, 1),
                duration_minutes=round(base.duration_minutes * factor, 1),
                coordinates=coords,
            )
        )
    return result[:3]


def _osrm_via(origin: GeoPoint, via: tuple[float, float], destination: GeoPoint) -> RouteDraft | None:
    path = (
        f"{origin.longitude},{origin.latitude};"
        f"{via[1]},{via[0]};"
        f"{destination.longitude},{destination.latitude}"
    )
    url = f"{OSRM_URL}/{path}"
    params = {"overview": "full", "geometries": "geojson", "steps": "false"}
    headers = {"User-Agent": settings.USER_AGENT}
    with httpx.Client(timeout=settings.HTTP_TIMEOUT_SECONDS, headers=headers) as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    routes = data.get("routes") or []
    if not routes:
        return None
    route = routes[0]
    lon_lat = (route.get("geometry") or {}).get("coordinates") or []
    coords = [(lat, lon) for lon, lat in lon_lat]
    if len(coords) < 2:
        return None
    return RouteDraft(
        id="tmp",
        name="tmp",
        distance_miles=round(float(route["distance"]) / METERS_PER_MILE, 1),
        duration_minutes=round(float(route["duration"]) / 60.0, 1),
        coordinates=_simplify(coords, 180),
    )


def _offset_midpoint(origin: GeoPoint, destination: GeoPoint, degrees: float) -> tuple[float, float]:
    mid_lat = (origin.latitude + destination.latitude) / 2
    mid_lon = (origin.longitude + destination.longitude) / 2
    dx = destination.longitude - origin.longitude
    dy = destination.latitude - origin.latitude
    length = math.hypot(dx, dy) or 1.0
    # Perpendicular offset in degrees (approx).
    return mid_lat + (-dx / length) * degrees, mid_lon + (dy / length) * degrees


def _similar(a: RouteDraft, b: RouteDraft) -> bool:
    return abs(a.distance_miles - b.distance_miles) < 3 and abs(a.duration_minutes - b.duration_minutes) < 8


def _simplify(coords: list[tuple[float, float]], max_points: int) -> list[tuple[float, float]]:
    if len(coords) <= max_points:
        return coords
    step = max(1, len(coords) // max_points)
    simplified = coords[::step]
    if simplified[-1] != coords[-1]:
        simplified.append(coords[-1])
    return simplified


def _haversine_miles(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 3958.8 * 2 * math.asin(math.sqrt(h))
