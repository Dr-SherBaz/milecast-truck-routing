from __future__ import annotations

import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PlanRequestSerializer
from .services.geocoding import GeocodingError
from .services.planner import build_plan
from .services.routing import RoutingError
from .services.weather import WeatherError

logger = logging.getLogger(__name__)


class HealthView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request: Request) -> Response:
        return Response({"status": "ok", "service": "milecast-django", "stack": "django+drf"})


class PlanView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def post(self, request: Request) -> Response:
        serializer = PlanRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            plan = build_plan(
                origin=data["origin"],
                destination=data["destination"],
                departure_time=data["departure_time"],
                load_weight_lb=data["load_weight_lb"],
                checkpoint_interval_miles=int(data["checkpoint_interval_miles"]),
                forecast_offset_hours=int(data["forecast_offset_hours"]),
            )
        except (GeocodingError, RoutingError, WeatherError, ValueError) as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.exception("Unexpected planner failure")
            return Response(
                {"detail": "Unable to build a weather-aware plan right now."},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response(plan)
