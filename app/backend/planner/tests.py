from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from rest_framework.test import APIRequestFactory

from planner.services.geocoding import GeoPoint
from planner.services.ranking import rank_routes
from planner.services.risk import RiskLevel, WeatherSample, classify_weather
from planner.services.routing import RouteDraft
from planner.views import PlanView


class RiskRuleTests(SimpleTestCase):
    def test_wind_rain_snow_thresholds(self):
        self.assertEqual(classify_weather(WeatherSample(24.9, 0, 0, 50), 10_000).level, RiskLevel.LOW)
        self.assertEqual(classify_weather(WeatherSample(25, 0, 0, 50), 10_000).level, RiskLevel.MODERATE)
        self.assertEqual(classify_weather(WeatherSample(35, 0, 0, 50), 10_000).level, RiskLevel.HIGH)
        self.assertEqual(classify_weather(WeatherSample(45, 0, 0, 50), 10_000).level, RiskLevel.SEVERE)
        self.assertEqual(classify_weather(WeatherSample(55, 0, 0, 50), 10_000).level, RiskLevel.NO_TRAVEL)
        self.assertEqual(classify_weather(WeatherSample(10, 1.01, 0, 50), 10_000).level, RiskLevel.NO_TRAVEL)
        self.assertEqual(classify_weather(WeatherSample(10, 0, 3.01, 50), 10_000).level, RiskLevel.NO_TRAVEL)

    def test_load_overrides(self):
        self.assertEqual(classify_weather(WeatherSample(50, 0, 0, 50), 30_001).level, RiskLevel.NO_TRAVEL)
        self.assertEqual(classify_weather(WeatherSample(40, 0, 0, 50), 40_001).level, RiskLevel.SEVERE)
        self.assertEqual(classify_weather(WeatherSample(50, 0, 0, 50), 30_000).level, RiskLevel.SEVERE)


class RankingTests(SimpleTestCase):
    def test_prefers_fewer_severe_then_high_then_time(self):
        safer = {
            "id": "a",
            "name": "A",
            "duration_minutes": 400,
            "summary": {
                "no_travel_miles": 0,
                "severe_miles": 5,
                "high_miles": 20,
                "average_risk": 1.2,
            },
        }
        riskier = {
            "id": "b",
            "name": "B",
            "duration_minutes": 300,
            "summary": {
                "no_travel_miles": 0,
                "severe_miles": 12,
                "high_miles": 5,
                "average_risk": 0.8,
            },
        }
        ranked = rank_routes([riskier, safer])
        self.assertEqual(ranked[0]["id"], "a")


@override_settings(ORS_API_KEY="")
class PlanApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch("planner.services.planner.forecast_at")
    @patch("planner.services.planner.get_three_routes")
    @patch("planner.services.planner.geocode_place")
    def test_plan_returns_three_routes(self, geocode, routes, weather):
        geocode.side_effect = [
            GeoPoint("Denver", 39.74, -104.99),
            GeoPoint("Chicago", 41.88, -87.63),
        ]
        routes.return_value = [
            RouteDraft("route-1", "Prairie corridor", 900, 980, [(39.74, -104.99), (41.88, -87.63)]),
            RouteDraft("route-2", "Ridge corridor", 920, 1000, [(39.74, -104.99), (40.5, -96.0), (41.88, -87.63)]),
            RouteDraft("route-3", "River corridor", 950, 1040, [(39.74, -104.99), (38.5, -96.0), (41.88, -87.63)]),
        ]
        weather.return_value = WeatherSample(18, 0.02, 0, 55)

        payload = {
            "origin": "Denver, CO",
            "destination": "Chicago, IL",
            "departure_time": datetime.now(timezone.utc).isoformat(),
            "load_weight_lb": 28000,
            "checkpoint_interval_miles": 50,
            "forecast_offset_hours": 0,
        }
        request = self.factory.post("/api/plan", payload, format="json")
        response = PlanView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        body = response.data
        self.assertEqual(len(body["routes"]), 3)
        self.assertEqual(body["forecast_window_hours"], 48)
        self.assertTrue(body["recommended_route_id"])
        self.assertTrue(body["corridor_heatmap"])

    def test_invalid_interval_rejected(self):
        payload = {
            "origin": "A",
            "destination": "B",
            "departure_time": datetime.now(timezone.utc).isoformat(),
            "load_weight_lb": 1,
            "checkpoint_interval_miles": 15,
        }
        request = self.factory.post("/api/plan", payload, format="json")
        response = PlanView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_forecast_window_validation(self):
        payload = {
            "origin": "A",
            "destination": "B",
            "departure_time": datetime.now(timezone.utc).isoformat(),
            "load_weight_lb": 1,
            "forecast_offset_hours": 49,
        }
        request = self.factory.post("/api/plan", payload, format="json")
        response = PlanView.as_view()(request)
        self.assertEqual(response.status_code, 400)
