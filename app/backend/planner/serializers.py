from __future__ import annotations

from rest_framework import serializers


class PlanRequestSerializer(serializers.Serializer):
    origin = serializers.CharField(min_length=2, max_length=160)
    destination = serializers.CharField(min_length=2, max_length=160)
    departure_time = serializers.DateTimeField()
    load_weight_lb = serializers.IntegerField(min_value=1, max_value=100_000)
    checkpoint_interval_miles = serializers.ChoiceField(choices=[10, 25, 50], default=25)
    forecast_offset_hours = serializers.IntegerField(min_value=0, max_value=48, default=0)

    def validate_origin(self, value: str) -> str:
        return value.strip()

    def validate_destination(self, value: str) -> str:
        return value.strip()
