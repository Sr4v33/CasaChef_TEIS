from __future__ import annotations

from typing import Any, Dict, List, Optional

from recommendations.domain.ports import AllyMenuPort, CountryInfoPort
from recommendations.infrastructure.adapters import ThirdPartyUnavailable


class RecommendationService:
    """Caso de uso principal del microservicio Flask.

    Es intencionalmente liviano: toma señales de entrada y devuelve
    recomendaciones de negocio sin depender de Django ORM.
    """

    def build_recommendations(
        self,
        *,
        city: Optional[str],
        budget: Optional[float],
        dish_type: Optional[str],
        limit: int = 3,
    ) -> Dict[str, Any]:
        catalog = self._base_catalog()

        if dish_type:
            normalized = dish_type.strip().lower()
            catalog = [item for item in catalog if normalized in item["tags"]]

        if budget is not None:
            catalog = [item for item in catalog if item["estimated_price"] <= budget]

        catalog = catalog[: max(1, min(limit, 10))]
        return {
            "service": "casachef-recommendations-service",
            "city": city or "no especificada",
            "filters": {
                "budget": budget,
                "dish_type": dish_type,
                "limit": limit,
            },
            "recommendations": catalog,
        }

    def capabilities(self) -> Dict[str, Any]:
        return {
            "service_to_provide": {
                "name": "CasaChef Recommendations API",
                "description": "Endpoint JSON con recomendaciones y capacidades relevantes del sistema.",
                "endpoints": [
                    "GET /api/v2/capabilities/",
                    "GET /api/v2/recommendations/",
                ],
            },
            "service_to_consume": {
                "name": "Servicio aliado de menú público",
                "configuration": "ALLY_SERVICE_BASE_URL + ALLY_MENU_ENDPOINT",
                "endpoint": "GET /api/v2/integrations/ally/menu/",
            },
            "third_party_api": {
                "name": "RestCountries vía RestCountriesAdapter",
                "endpoint": "GET /api/v2/integrations/third-party/country/<country_code>/",
                "pattern": "Adapter + inversión de dependencias",
            },
        }

    def _base_catalog(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "Bandeja casera ejecutiva",
                "tags": ["almuerzo", "tradicional", "alto-proteina"],
                "estimated_price": 26000,
                "reason": "Buena relación precio/cantidad para jornada laboral.",
            },
            {
                "name": "Menú vegetariano de temporada",
                "tags": ["almuerzo", "vegetariano", "saludable"],
                "estimated_price": 24000,
                "reason": "Opción con menor complejidad logística y alta rotación diaria.",
            },
            {
                "name": "Cena casera premium",
                "tags": ["cena", "premium", "tradicional"],
                "estimated_price": 42000,
                "reason": "Recomendada para pedidos programados y producción limitada.",
            },
            {
                "name": "Desayuno artesanal",
                "tags": ["desayuno", "artesanal", "economico"],
                "estimated_price": 18000,
                "reason": "Bajo costo y preparación simple para cocineros nuevos.",
            },
        ]


class IntegrationFacade:
    """Facade de integración para ocultar al controlador la topología externa."""

    def __init__(
        self,
        *,
        recommendation_service: RecommendationService,
        country_info: CountryInfoPort,
        ally_menu: AllyMenuPort,
    ) -> None:
        self._recommendation_service = recommendation_service
        self._country_info = country_info
        self._ally_menu = ally_menu

    def ally_menu(self, city: Optional[str] = None) -> Dict[str, Any]:
        return self._ally_menu.get_public_menu(city=city)

    def country_context(self, country_code: str) -> Dict[str, Any]:
        try:
            return self._country_info.get_country_context(country_code)
        except ThirdPartyUnavailable as exc:
            return {
                "provider": "fallback",
                "country_code": country_code.strip().upper(),
                "message": "API de terceros no disponible; se retorna contexto mínimo controlado.",
                "detail": str(exc),
            }

    def integrated_summary(
        self,
        *,
        country_code: str,
        city: Optional[str],
        budget: Optional[float],
        dish_type: Optional[str],
    ) -> Dict[str, Any]:
        return {
            "recommendations": self._recommendation_service.build_recommendations(
                city=city,
                budget=budget,
                dish_type=dish_type,
            ),
            "ally_menu": self.ally_menu(city=city),
            "country_context": self.country_context(country_code),
        }
