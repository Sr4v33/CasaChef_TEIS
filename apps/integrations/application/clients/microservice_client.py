from __future__ import annotations

from typing import Any, Dict, Optional

import requests
from django.conf import settings


class MicroserviceUnavailable(Exception):
    pass


class RecommendationsMicroserviceClient:
    """Cliente HTTP para consumir el microservicio Flask desde Django.

    La vista de Django no conoce rutas internas de Flask excepto a través de este
    cliente, manteniendo una frontera clara entre monolito y microservicio.
    """

    def __init__(self, base_url: Optional[str] = None, timeout_seconds: Optional[float] = None) -> None:
        self._base_url = (base_url or settings.RECOMMENDATIONS_SERVICE_URL).rstrip("/")
        self._timeout = timeout_seconds or settings.INTEGRATION_HTTP_TIMEOUT

    def health(self) -> Dict[str, Any]:
        return self._get("/health/ready")

    def capabilities(self) -> Dict[str, Any]:
        return self._get("/api/v2/capabilities/")

    def recommendations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._get("/api/v2/recommendations/", params=params)

    def ally_menu(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._get("/api/v2/integrations/ally/menu/", params=params)

    def country_context(self, country_code: str) -> Dict[str, Any]:
        return self._get(f"/api/v2/integrations/third-party/country/{country_code}/")

    def summary(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._get("/api/v2/integrations/summary/", params=params)

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response = requests.get(f"{self._base_url}{path}", params=params, timeout=self._timeout)
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            raise MicroserviceUnavailable(str(exc)) from exc
        except ValueError as exc:
            raise MicroserviceUnavailable("El microservicio no respondió JSON válido") from exc

        if not isinstance(payload, dict):
            raise MicroserviceUnavailable("Contrato inválido: se esperaba un objeto JSON")
        return payload
