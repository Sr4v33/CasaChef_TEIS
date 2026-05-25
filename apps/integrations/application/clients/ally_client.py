from __future__ import annotations
import requests
from django.conf import settings


class AllyServiceUnavailable(Exception):
    pass


class AllySystemInfoClient:
    """
    Consume el endpoint público del equipo aliado.
    GET http://3.94.94.27/api/v1/system/info/
    """

    def __init__(self) -> None:
        self._base_url = settings.ALLY_SERVICE_BASE_URL.rstrip("/")
        self._timeout = settings.INTEGRATION_HTTP_TIMEOUT

    def get_system_info(self) -> dict:
        if not self._base_url:
            return {
                "status": "not_configured",
                "message": "ALLY_SERVICE_BASE_URL no está configurado.",
            }
        try:
            response = requests.get(
                f"{self._base_url}/api/v1/system/info/",
                timeout=self._timeout,
            )
            response.raise_for_status()
            return {"status": "ok", "data": response.json()}
        except requests.RequestException as exc:
            raise AllyServiceUnavailable(str(exc)) from exc