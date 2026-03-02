from django.db import transaction

from apps.orders.domain.builders.order_builder import OrderBuilder
from apps.orders.domain.exceptions import OrderDomainError
from apps.orders.domain.ports.order_repository_port import OrderRepository
from apps.orders.domain.ports.production_repository_port import ProductionRepository
from apps.orders.infrastructure.factories.notifier_factory import Notifier


class OrderService:
    """Service Layer para casos de uso de Order.

    Orquesta flujos delegando lógica de negocio a OrderEntity y OrderBuilder.
    Recibe dependencias por inyección para facilitar tests sin infraestructura.
    """

    def __init__(
        self,
        order_repo: OrderRepository,
        production_repo: ProductionRepository,
        notifier: Notifier,
    ) -> None:
        self._order_repo = order_repo
        self._production_repo = production_repo
        self._notifier = notifier

    def create_order(self, user, data: dict) -> int:
        """Crea una orden y reserva producción dentro de una transacción atómica."""
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

    def confirm_order(self, order_id: int) -> None:
        """Confirma una orden pendiente. La transición de estado vive en OrderEntity."""
        order = self._get_order_or_raise(order_id)
        order.confirm()                              # lógica en la entidad, no aquí
        self._order_repo.update(order)
        self._notifier.send_order_confirmed(order_id)

    def cancel_order(self, order_id: int) -> None:
        """Cancela una orden. La transición de estado vive en OrderEntity."""
        order = self._get_order_or_raise(order_id)
        order.cancel()                               # lógica en la entidad, no aquí
        self._order_repo.update(order)
        self._notifier.send_order_cancelled(order_id)

    def validate_stock(self, order_id: int) -> None:
        """Verifica stock para todos los ítems sin reservar."""
        order = self._get_order_or_raise(order_id)
        for item in order.items:
            if not self._production_repo.check_stock(item.dish_id, item.quantity):
                raise OrderDomainError(
                    f"Stock insuficiente para el plato {item.dish_id}"
                )

    # --------------------------------------------------
    # Helpers privados
    # --------------------------------------------------

    def _get_order_or_raise(self, order_id: int):
        order = self._order_repo.get_by_id(order_id)
        if order is None:
            raise OrderDomainError(f"Orden {order_id} no encontrada")
        return order