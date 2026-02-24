from apps.orders.domain.ports.production_repository_port import ProductionRepository
from apps.production.models import DailyProduction


class DjangoProductionRepository(ProductionRepository):

    def check_and_reserve(self, dish_id: int, date, quantity: int):
        production = (
            DailyProduction.objects
            .select_for_update()
            .get(dish_id=dish_id, date=date)
        )

        if production.available_units < quantity:
            raise ValueError(f"Cupos insuficientes para el plato {dish_id}")

        production.available_units -= quantity
        production.save()


