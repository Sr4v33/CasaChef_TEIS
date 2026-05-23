from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from recommendations.domain.ports import AllyMenuPort, CountryInfoPort


class ThirdPartyUnavailable(Exception):
    """Error controlado para fallos de integraciones externas."""


class RestCountriesAdapter(CountryInfoPort):
    """Adapter de API de terceros.

    El dominio pide `get_country_context`; este adapter traduce ese contrato a la
    API real de RestCountries. Si mañana cambia el proveedor, se cambia este
    archivo y no el servicio de aplicación.
    """

    def __init__(self, base_url: str, timeout_seconds: float = 3) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout_seconds

    def get_country_context(self, country_code: str) -> Dict[str, Any]:
        normalized_code = country_code.strip().upper()
        if not normalized_code:
            raise ValueError("country_code es obligatorio")

        url = f"{self._base_url}/{normalized_code}"
        try:
            response = requests.get(url, timeout=self._timeout)
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            raise ThirdPartyUnavailable(str(exc)) from exc

        if not isinstance(payload, list) or not payload:
            raise ThirdPartyUnavailable("La API de terceros no retornó un país válido")

        country = payload[0]
        currencies = country.get("currencies", {}) or {}
        currency_code = next(iter(currencies.keys()), None)
        currency_name = currencies.get(currency_code, {}).get("name") if currency_code else None
        languages = list((country.get("languages", {}) or {}).values())

        return {
            "provider": "restcountries",
            "country_code": normalized_code,
            "country_name": country.get("name", {}).get("common"),
            "currency_code": currency_code,
            "currency_name": currency_name,
            "languages": languages,
            "region": country.get("region"),
        }


class AllyMenuHttpClient(AllyMenuPort):
    """Cliente HTTP para consumir el servicio del equipo aliado.

    El endpoint real se define por variables de entorno para no acoplar CasaChef
    a una IP o ruta fija durante la sustentación.
    """

    def __init__(self, base_url: str, endpoint: str, timeout_seconds: float = 3) -> None:
        self._base_url = base_url.rstrip("/")
        self._endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        self._timeout = timeout_seconds

    def get_public_menu(self, city: Optional[str] = None) -> Dict[str, Any]:
        if not self._base_url:
            return {
                "status": "not_configured",
                "source": "fallback",
                "message": "Configure ALLY_SERVICE_BASE_URL para consumir el servicio aliado real.",
                "items": [
                    {
                        "name": "Menú aliado de demostración",
                        "category": "fallback",
                        "estimated_price": 25000,
                    }
                ],
            }

        params: Dict[str, Any] = {}
        if city:
            params["city"] = city

        try:
            response = requests.get(
                f"{self._base_url}{self._endpoint}",
                params=params,
                timeout=self._timeout,
            )
            response.raise_for_status()
            return {
                "status": "ok",
                "source": self._base_url,
                "payload": response.json(),
            }
        except requests.RequestException as exc:
            return {
                "status": "unavailable",
                "source": self._base_url,
                "message": str(exc),
                "items": [],
            }
