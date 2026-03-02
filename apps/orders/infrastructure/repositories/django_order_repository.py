from typing import Optional

from django.db import transaction
from django.utils import timezone

from apps.orders.domain.entities.order import OrderEntity
from apps.orders.domain.entities.order_item import OrderItemEntity
from apps.orders.domain.ports.order_repository_port import OrderRepository
from apps.orders.infrastructure.models.order_item_model import OrderItem
from apps.orders.infrastructure.models.order_model import Order


class DjangoOrderRepository(OrderRepository):

    @transaction.atomic
    def save(self, order: OrderEntity) -> int:
        order_model = Order.objects.create(
            user_id=order.user_id,
            address=order.address,
            status=order.status,
            orderNumber=getattr(order, "order_number", ""),
        )
        for item in order.items:
            OrderItem.objects.create(
                order=order_model,
                dish_id=item.dish_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        return order_model.pk

    def get_by_id(self, order_id: int) -> Optional[OrderEntity]:
        try:
            model = Order.objects.prefetch_related("items").get(pk=order_id)
        except Order.DoesNotExist:
            return None

        items = [
            OrderItemEntity(
                dish_id=item.dish_id,
                quantity=item.quantity,
                unit_price=float(item.unit_price),
            )
            for item in model.items.all() # type: ignore[attr-defined]
        ]
        return OrderEntity(
            user_id=model.user_id,  # type: ignore[attr-defined]
            address=model.address,
            date=str(model.created_at.date()),
            items=items,
            status=model.status,
        )

    @transaction.atomic
    def update(self, order: OrderEntity) -> None:
        Order.objects.filter(pk=getattr(order, "order_id", None)).update(
            status=order.status,
            updated_at=timezone.now(),
        )