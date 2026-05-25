from apps.orders.domain.exceptions import InsufficientProductionStock
from apps.orders.domain.ports.production_repository_port import ProductionRepository
from apps.production.infrastructure.models.daily_production_model import DailyProductionModel
from django.utils.translation import gettext_lazy as _


class DjangoProductionRepository(ProductionRepository):

    def check_and_reserve(self, dish_id: int, date, quantity: int) -> None:
        try:
            production = (
                DailyProductionModel.objects
                .select_for_update()
                .get(dish_id=dish_id, date=date)
            )
        except DailyProductionModel.DoesNotExist:
            raise InsufficientProductionStock(
                _(
                    "No hay producción registrada para el plato %(dish_id)s "
                    "en la fecha %(date)s."
                )
                % {"dish_id": dish_id, "date": date}
            )
        if production.available_units < quantity:
            raise InsufficientProductionStock(
                _("Cupos insuficientes para el plato %(dish_id)s")
                % {"dish_id": dish_id}
            )
        production.available_units -= quantity
        production.save()

    def check_stock(self, dish_id: int, date: str, quantity: int) -> bool:
        """Comprueba que el plan del día cubre la cantidad en esa fecha.

        Si el pedido ya reservó cupos al crearse, ``available_units`` es lo que
        queda después de descontar; se suma ``quantity`` para no marcar conflicto.
        """
        try:
            production = DailyProductionModel.objects.get(dish_id=dish_id, date=date)
        except DailyProductionModel.DoesNotExist:
            return False
        return production.available_units + quantity >= quantity
