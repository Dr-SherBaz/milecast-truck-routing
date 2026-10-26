from __future__ import annotations

import logging
from dataclasses import dataclass

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


@dataclass(frozen=True)
class GeoPoint:
    label: str
    latitude: float
    longitude: float


class GeocodingError(Exception):
    pass


def geocode_place(query: str) -> GeoPoint:
    cleaned = query.strip()
    if len(cleaned) < 2:
        raise GeocodingError("Origin and destination must be at least 2 characters.")

    params = {
        "q": cleaned,
        "format": "json",
        "limit": 1,
        "addressdetails": 0,
    }
    headers = {"User-Agent": settings.USER_AGENT}

    try:
        with httpx.Client(timeout=settings.HTTP_TIMEOUT_SECONDS, headers=headers) as client:
            response = client.get(NOMINATIM_URL, params=params)
            response.raise_for_status()
            payload = response.json()
    except httpx.HTTPError as exc:
        raise GeocodingError(f"Unable to geocode '{cleaned}'.") from exc

    if not payload:
        raise GeocodingError(f"No match found for '{cleaned}'. Try city and state.")

    hit = payload[0]
    return GeoPoint(
        label=hit.get("display_name", cleaned),
        latitude=float(hit["lat"]),
        longitude=float(hit["lon"]),
    )
