from typing import List, Optional

from apps.production.domain.entities.daily_production import DailyProductionEntity
from apps.production.domain.ports.production_repository_port import ProductionRepositoryPort
from apps.production.infrastructure.models.daily_production_model import DailyProductionModel


class DjangoProductionRepository(ProductionRepositoryPort):
    """Implementación Django ORM del repositorio de producción diaria."""

    def save(self, production: DailyProductionEntity) -> DailyProductionEntity:
        model = DailyProductionModel.objects.create(
            dish_id=production.dish_id,
            date=production.date,
            available_units=production.available_units,
        )
        production.production_id = model.pk
        return production

    def get_by_id(self, production_id: int) -> Optional[DailyProductionEntity]:
        try:
            model = DailyProductionModel.objects.get(pk=production_id)
        except DailyProductionModel.DoesNotExist:
            return None
        return self._to_entity(model)

    def get_by_dish_and_date(self, dish_id: int, date: str) -> Optional[DailyProductionEntity]:
        try:
            model = DailyProductionModel.objects.get(dish_id=dish_id, date=date)
        except DailyProductionModel.DoesNotExist:
            return None
        return self._to_entity(model)

    def list(self, dish_id: Optional[int] = None, date: Optional[str] = None) -> List[DailyProductionEntity]:
        qs = DailyProductionModel.objects.all()
        if dish_id is not None:
            qs = qs.filter(dish_id=dish_id)
        if date is not None:
            qs = qs.filter(date=date)
        return [self._to_entity(m) for m in qs]

    def update(self, production: DailyProductionEntity) -> DailyProductionEntity:
        DailyProductionModel.objects.filter(pk=production.production_id).update(
            available_units=production.available_units,
        )
        return production

    @staticmethod
    def _to_entity(model: DailyProductionModel) -> DailyProductionEntity:
        return DailyProductionEntity(
            production_id=model.pk,
            dish_id=model.dish_id,
            date=str(model.date),
            available_units=model.available_units,
        )
