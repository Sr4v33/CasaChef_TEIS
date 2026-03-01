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
                .orderNumber()
                .build()
            )

            order_id = self._order_repo.save(order_entity)

        self._notifier.send_order_confirmation(order_id)
        return order_id
    
    def calculateTotal(self):
        total=sum(item.calculateSubtotal() for item in self.items.all())
        self.total=total
        return self.total
    
    def calculateSubtotal(self):
        return self.quantity * self.price
    
    def confirm_order(self, order_id):
        order = self._order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Orden no encontrada")
        order.status = "CONFIRMED"
        self._order_repo.update(order)
        self._notifier.send_order_confirmed(order_id)
    
    def cancel_order(self, order_id):
        order = self._order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Orden no encontrada")
        order.status = "CANCELLED"
        self._order_repo.update(order)
        self._notifier.send_order_cancelled(order_id)

    def validate_stock(self, order_id):
        order = self._order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Orden no encontrada")
        for item in order.items:
            if not self._production_repo.check_stock(item.dish_id, item.quantity):
                raise ValueError(f"Stock insuficiente para el plato {item.dish_id}")
            
#pending: assign cook
            
    