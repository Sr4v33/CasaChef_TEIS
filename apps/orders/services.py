# apps/orders/services.py
from orders.domain.order_builder import OrderBuilder
from orders.infra.repositories import (
    DjangoOrderRepository,
    DjangoProductionRepository,
)
from orders.infra.notifier_factory import NotifierFactory


class OrderService:

    def __init__(self):
        self._order_repo = DjangoOrderRepository()
        self._production_repo = DjangoProductionRepository()
        self._notifier = NotifierFactory.create()

    def create_order(self, user, data) -> int:
        builder = OrderBuilder(self._production_repo)

        order_entity = (
            builder
            .for_user(user.id)
            .with_items(data["items"])
            .to_address(data["address"])
            .for_date(data["date"])
            .build()
        )

        order_id = self._order_repo.save(order_entity)

        self._notifier.send_order_confirmation(order_id)

        return order_id
