from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class RiskLevel(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    severe = "severe"
    no_travel = "no_travel"


class PlanRequest(BaseModel):
    origin: str = Field(min_length=2, max_length=120)
    destination: str = Field(min_length=2, max_length=120)
    departure_time: datetime
    load_weight_lb: int = Field(gt=0, le=100_000)
    checkpoint_interval_miles: Literal[10, 25, 50] = 25
    forecast_offset_hours: int = Field(default=0, ge=0, le=48)

    @field_validator("origin", "destination")
    @classmethod
    def strip_location(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Location cannot be blank")
        return value


class WeatherPoint(BaseModel):
    wind_mph: float = Field(ge=0)
    rain_in_hr: float = Field(ge=0)
    snow_in_hr: float = Field(ge=0)
    temperature_f: float


class Checkpoint(BaseModel):
    mile: float = Field(ge=0)
    latitude: float
    longitude: float
    eta: datetime
    forecast_offset_hours: int = Field(ge=0, le=48)
    weather: WeatherPoint
    risk_level: RiskLevel
    risk_score: float = Field(ge=0)
    risk_reasons: list[str]


class RouteSummary(BaseModel):
    low_miles: float = Field(ge=0)
    moderate_miles: float = Field(ge=0)
    high_miles: float = Field(ge=0)
    severe_miles: float = Field(ge=0)
    no_travel_miles: float = Field(ge=0)
    average_risk: float = Field(ge=0)


class Route(BaseModel):
    id: str
    name: str
    distance_miles: float = Field(gt=0)
    duration_minutes: float = Field(gt=0)
    coordinates: list[tuple[float, float]] = Field(min_length=2)
    checkpoints: list[Checkpoint]
    summary: RouteSummary


class PlanResponse(BaseModel):
    request: PlanRequest
    routes: list[Route] = Field(min_length=3, max_length=3)
    recommended_route_id: str
    recommendation_reason: str
    corridor_heatmap: list[Checkpoint]
    forecast_window_hours: int = 48

    @field_validator("routes")
    @classmethod
    def require_three_routes(cls, value: list[Route]) -> list[Route]:
        if len(value) != 3:
            raise ValueError("The planner must return exactly three route alternatives")
        return value
