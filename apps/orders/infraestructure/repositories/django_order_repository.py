from django.db import transaction

from apps.orders.infraestructure.models.order_model import Order
from apps.orders.infraestructure.models.order_item_model import OrderItem
from apps.orders.domain.ports.order_repository_port import OrderRepository
from apps.orders.domain.entities.order import OrderEntity

from django.utils import timezone

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
