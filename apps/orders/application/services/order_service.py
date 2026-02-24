from apps.orders.domain.builders.order_builder import OrderBuilder
from apps.orders.infraestructure.repositories.django_order_repository import DjangoOrderRepository
from apps.orders.infraestructure.repositories.django_production_repository import DjangoProductionRepository
from apps.orders.infraestructure.factories.notifier_factory import NotifierFactory
from django.db import transaction

class OrderService:

    def __init__(self, order_repo, production_repo, notifier):
        self._order_repo = DjangoOrderRepository()
        self._production_repo = DjangoProductionRepository()
        self._notifier = NotifierFactory.create()

    def create_order(self, user, data) -> int:

        with transaction.atomic():
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
