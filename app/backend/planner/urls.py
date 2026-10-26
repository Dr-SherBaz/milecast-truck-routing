from django.urls import path

from .views import HealthView, PlanView

urlpatterns = [
    path("health", HealthView.as_view(), name="health"),
    path("api/plan", PlanView.as_view(), name="plan"),
]
