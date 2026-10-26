from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .checkpoints import build_checkpoints
from .models import Checkpoint, PlanRequest, PlanResponse, Route, RiskLevel
from .ranking import rank_routes
from .risk import summarize_risks
from .routing import MockRoutingProvider
from .weather import MockWeatherProvider

app = FastAPI(title="Weather-Aware Truck Routing", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
routing_provider = MockRoutingProvider()
weather_provider = MockWeatherProvider()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "provider_mode": "mock"}


@app.post("/api/plan", response_model=PlanResponse)
def create_plan(request: PlanRequest) -> PlanResponse:
    drafts = routing_provider.get_alternatives(request.origin, request.destination)
    if len(drafts) != 3:
        raise HTTPException(status_code=502, detail="Routing provider must return exactly three alternatives")
    routes: list[Route] = []
    for draft in drafts:
        checkpoints = build_checkpoints(draft, request.departure_time, request.checkpoint_interval_miles, request.load_weight_lb, request.forecast_offset_hours, weather_provider)
        levels = [(checkpoint.risk_level, _segment_miles(checkpoints, index, draft.distance_miles)) for index, checkpoint in enumerate(checkpoints)]
        routes.append(Route(id=draft.id, name=draft.name, distance_miles=draft.distance_miles, duration_minutes=draft.duration_minutes, coordinates=draft.coordinates, checkpoints=checkpoints, summary=summarize_risks(levels)))
    ranked = rank_routes(routes)
    recommended = ranked[0]
    heatmap = _heatmap(ranked, request.forecast_offset_hours)
    return PlanResponse(request=request, routes=routes, recommended_route_id=recommended.id, recommendation_reason=_recommendation_reason(recommended), corridor_heatmap=heatmap)


def _segment_miles(checkpoints: list[Checkpoint], index: int, total: float) -> float:
    previous = checkpoints[index - 1].mile if index else 0
    return max(checkpoints[index].mile - previous, 0.1) if index < len(checkpoints) - 1 else max(total - previous, 0.1)


def _heatmap(routes: list[Route], offset: int) -> list[Checkpoint]:
    points: list[Checkpoint] = []
    for route in routes:
        points.extend(route.checkpoints)
    return [point.model_copy(update={"forecast_offset_hours": offset}) for point in points]


def _recommendation_reason(route: Route) -> str:
    summary = route.summary
    if summary.no_travel_miles:
        return f"{route.name} has the best available score, but includes {summary.no_travel_miles:.0f} miles marked no-travel. Recheck conditions before departure."
    return f"{route.name} is recommended using severe miles, high-risk miles, average risk, then travel time."
