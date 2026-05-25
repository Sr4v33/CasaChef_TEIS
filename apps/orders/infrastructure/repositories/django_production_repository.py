from apps.orders.domain.ports.production_repository_port import ProductionRepository
from apps.production.infrastructure.models.daily_production_model import DailyProductionModel
from django.utils.translation import gettext_lazy as _


class DjangoProductionRepository(ProductionRepository):

    def check_and_reserve(self, dish_id: int, date, quantity: int) -> None:
        production = (
            DailyProductionModel.objects
            .select_for_update()
            .get(dish_id=dish_id, date=date)
        )
        if production.available_units < quantity:
            raise ValueError(
                _("Cupos insuficientes para el plato %(dish_id)s")
                % {"dish_id": dish_id}
            )
        production.available_units -= quantity
        production.save()

    def check_stock(self, dish_id: int, quantity: int) -> bool:
        """Verifica sin reservar si hay stock disponible para cualquier fecha activa."""
        return DailyProductionModel.objects.filter(
            dish_id=dish_id,
            available_units__gte=quantity,
        ).exists()
