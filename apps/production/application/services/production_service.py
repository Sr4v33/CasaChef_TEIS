from typing import List, Optional

from apps.production.domain.entities.daily_production import DailyProductionEntity
from apps.production.domain.ports.production_repository_port import ProductionRepositoryPort


class ProductionService:
    """Service Layer para gestión de producción diaria.

    Orquesta los casos de uso sin contener lógica de negocio (que vive en la entidad).
    Cumple SRP: cada método es un caso de uso concreto.
    """

    def __init__(self, repo: ProductionRepositoryPort) -> None:
        self._repo = repo

    def create_production(
        self,
        *,
        dish_id: int,
        date: str,
        available_units: int,
    ) -> DailyProductionEntity:
        """Crea un nuevo registro de producción diaria para un plato."""
        existing = self._repo.get_by_dish_and_date(dish_id=dish_id, date=date)
        if existing is not None:
            raise ValueError(
                f"Ya existe un registro de producción para dish_id={dish_id} en fecha={date}"
            )
        production = DailyProductionEntity(
            dish_id=dish_id,
            date=date,
            available_units=available_units,
        )
        return self._repo.save(production)

    def get_production(self, production_id: int) -> Optional[DailyProductionEntity]:
        """Obtiene un registro de producción por su ID."""
        return self._repo.get_by_id(production_id)

    def list_productions(
        self,
        dish_id: Optional[int] = None,
        date: Optional[str] = None,
    ) -> List[DailyProductionEntity]:
        """Lista registros de producción, opcionalmente filtrados por plato y/o fecha."""
        return self._repo.list(dish_id=dish_id, date=date)

    def adjust_units(self, production_id: int, new_units: int) -> DailyProductionEntity:
        """Ajusta los cupos disponibles de un registro de producción."""
        production = self._repo.get_by_id(production_id)
        if production is None:
            raise ValueError(f"No existe producción con id={production_id}")
        production.adjust(new_units)
        return self._repo.update(production)
