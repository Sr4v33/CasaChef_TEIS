from abc import ABC, abstractmethod
from typing import List, Optional

from apps.production.domain.entities.daily_production import DailyProductionEntity


class ProductionRepositoryPort(ABC):

    @abstractmethod
    def save(self, production: DailyProductionEntity) -> DailyProductionEntity:
        ...

    @abstractmethod
    def get_by_id(self, production_id: int) -> Optional[DailyProductionEntity]:
        ...

    @abstractmethod
    def get_by_dish_and_date(self, dish_id: int, date: str) -> Optional[DailyProductionEntity]:
        ...

    @abstractmethod
    def list(self, dish_id: Optional[int] = None, date: Optional[str] = None) -> List[DailyProductionEntity]:
        ...

    @abstractmethod
    def update(self, production: DailyProductionEntity) -> DailyProductionEntity:
        ...
