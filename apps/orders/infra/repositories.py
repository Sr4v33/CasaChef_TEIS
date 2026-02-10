# apps/orders/infra/repositories.py
from django.db import transaction
from django.utils import timezone

from orders.models import Order, OrderItem
from production.models import DailyProduction

from orders.domain.ports import OrderRepository, ProductionRepository
from orders.domain.entities import OrderEntity


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


class DjangoOrderRepository(OrderRepository):

    @transaction.atomic
    def save(self, order: OrderEntity) -> int:
        order_model = Order.objects.create(
            user_id=order.user_id,
            address=order.address,
            status=order.status,
            created_at=timezone.now(),
        )

        for item in order.items:
            OrderItem.objects.create(
                order=order_model,
                dish_id=item.dish_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )

        return order_model.pk
