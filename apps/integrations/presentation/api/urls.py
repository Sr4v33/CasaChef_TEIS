from django.urls import path

from apps.integrations.presentation.api.views import (
    AllyMenuProxyView,
    CapabilitiesProxyView,
    CountryContextProxyView,
    IntegrationSummaryProxyView,
    IntegrationsRootView,
    MicroserviceHealthView,
    RecommendationsProxyView,
)

urlpatterns = [
    path("", IntegrationsRootView.as_view(), name="integrations-root"),
    path("microservice/health/", MicroserviceHealthView.as_view(), name="microservice-health"),
    path("capabilities/", CapabilitiesProxyView.as_view(), name="integration-capabilities"),
    path("recommendations/", RecommendationsProxyView.as_view(), name="recommendations-proxy"),
    path("ally-menu/", AllyMenuProxyView.as_view(), name="ally-menu-proxy"),
    path("country/<str:country_code>/", CountryContextProxyView.as_view(), name="country-context-proxy"),
    path("summary/", IntegrationSummaryProxyView.as_view(), name="integration-summary-proxy"),
]
