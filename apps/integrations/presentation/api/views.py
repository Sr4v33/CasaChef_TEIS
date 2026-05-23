from __future__ import annotations

from typing import Any, Dict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.integrations.application.clients.microservice_client import (
    MicroserviceUnavailable,
    RecommendationsMicroserviceClient,
)


def _client() -> RecommendationsMicroserviceClient:
    return RecommendationsMicroserviceClient()


def _query_params(request) -> Dict[str, Any]:
    return {key: value for key, value in request.query_params.items() if value not in (None, "")}


class IntegrationsRootView(APIView):
    """GET /api/integrations/ — Contrato de integraciones disponible en Django."""

    def get(self, request):
        return Response(
            {
                "microservice_health": request.build_absolute_uri("/api/integrations/microservice/health/"),
                "capabilities": request.build_absolute_uri("/api/integrations/capabilities/"),
                "recommendations": request.build_absolute_uri("/api/integrations/recommendations/"),
                "ally_menu": request.build_absolute_uri("/api/integrations/ally-menu/"),
                "country_context_example": request.build_absolute_uri("/api/integrations/country/CO/"),
                "summary": request.build_absolute_uri("/api/integrations/summary/"),
            },
            status=status.HTTP_200_OK,
        )


class MicroserviceHealthView(APIView):
    def get(self, request):
        try:
            return Response(_client().health(), status=status.HTTP_200_OK)
        except MicroserviceUnavailable as exc:
            return Response(
                {"status": "unavailable", "error": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class CapabilitiesProxyView(APIView):
    def get(self, request):
        try:
            return Response(_client().capabilities(), status=status.HTTP_200_OK)
        except MicroserviceUnavailable as exc:
            return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RecommendationsProxyView(APIView):
    def get(self, request):
        try:
            return Response(_client().recommendations(_query_params(request)), status=status.HTTP_200_OK)
        except MicroserviceUnavailable as exc:
            return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class AllyMenuProxyView(APIView):
    def get(self, request):
        try:
            return Response(_client().ally_menu(_query_params(request)), status=status.HTTP_200_OK)
        except MicroserviceUnavailable as exc:
            return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CountryContextProxyView(APIView):
    def get(self, request, country_code: str):
        try:
            return Response(_client().country_context(country_code), status=status.HTTP_200_OK)
        except MicroserviceUnavailable as exc:
            return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class IntegrationSummaryProxyView(APIView):
    def get(self, request):
        try:
            return Response(_client().summary(_query_params(request)), status=status.HTTP_200_OK)
        except MicroserviceUnavailable as exc:
            return Response({"error": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
