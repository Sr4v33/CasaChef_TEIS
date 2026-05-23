from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class CountryInfoPort(ABC):
    """Contrato que el negocio conoce para obtener contexto de país.

    La implementación concreta puede ser RestCountries, una API paga o un mock.
    """

    @abstractmethod
    def get_country_context(self, country_code: str) -> Dict[str, Any]:
        raise NotImplementedError


class AllyMenuPort(ABC):
    """Contrato para consumir el servicio del equipo aliado."""

    @abstractmethod
    def get_public_menu(self, city: Optional[str] = None) -> Dict[str, Any]:
        raise NotImplementedError
