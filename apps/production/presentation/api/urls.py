from django.urls import path
from apps.production.presentation.api.views import (
    ProductionListCreateView,
    ProductionDetailView,
)

urlpatterns = [
    path("",          ProductionListCreateView.as_view(), name="production-list-create"),
    path("<int:production_id>/", ProductionDetailView.as_view(),    name="production-detail"),
]
