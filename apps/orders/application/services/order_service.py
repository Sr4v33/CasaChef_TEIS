import logging
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.orders.domain.builders.order_builder import OrderBuilder
from apps.orders.domain.entities.order import OrderEntity
from apps.orders.domain.exceptions import OrderDomainError, OrderNotFoundError
from apps.orders.domain.ports.order_repository_port import OrderRepository
from apps.orders.domain.ports.production_repository_port import ProductionRepository
from apps.orders.infrastructure.tasks.notification_tasks import (
    build_daily_order_report,
    send_order_notification,
)
from typing import Optional

logger = logging.getLogger(__name__)


class OrderService:
    """Service Layer para casos de uso de Order.

    Orquesta flujos delegando lógica de negocio a OrderEntity y OrderBuilder.
    Recibe dependencias por inyección para facilitar tests sin infraestructura.
    Expone métodos públicos para todos los casos de uso: ninguna vista debe
    acceder a los atributos privados de este servicio.
    """

    def __init__(
        self,
        order_repo: OrderRepository,
        production_repo: ProductionRepository,
    ) -> None:
        self._order_repo = order_repo
        self._production_repo = production_repo

    # ──────────────────────────────────────────────
    # Casos de uso públicos
    # ──────────────────────────────────────────────

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

        self._queue_order_event(order_id, "CREATED")
        self._queue_daily_report(order_entity.date)
        return order_id

    def get_order(self, order_id: int) -> Optional[OrderEntity]:
        """Retorna la entidad Order o None si no existe.

        Las vistas deben usar este método en lugar de acceder a _order_repo directamente.
        """
        return self._order_repo.get_by_id(order_id)

    def confirm_order(self, order_id: int) -> None:
        """Confirma una orden pendiente. La transición de estado vive en OrderEntity."""
        order = self._get_order_or_raise(order_id)
        order.confirm()
        self._order_repo.update(order)
        self._queue_order_event(order_id, "CONFIRMED")
        self._queue_daily_report(order.date)

    def cancel_order(self, order_id: int) -> None:
        """Cancela una orden. La transición de estado vive en OrderEntity."""
        order = self._get_order_or_raise(order_id)
        order.cancel()
        self._order_repo.update(order)
        self._queue_order_event(order_id, "CANCELLED")
        self._queue_daily_report(order.date)

    def validate_stock(self, order_id: int) -> None:
        """Verifica que el plan del día de la orden sigue cubriendo cada ítem."""
        order = self._get_order_or_raise(order_id)
        if not order.date:
            raise OrderDomainError(_("La orden no tiene fecha de entrega."))

        for item in order.items:
            if not self._production_repo.check_stock(
                item.dish_id, order.date, item.quantity
            ):
                raise OrderDomainError(
                    _(
                        "Sin plan o cupos insuficientes para el plato %(dish_id)s "
                        "en la fecha %(date)s"
                    )
                    % {"dish_id": item.dish_id, "date": order.date}
                )

    # ──────────────────────────────────────────────
    # Helpers privados
    # ──────────────────────────────────────────────

    def _get_order_or_raise(self, order_id: int) -> OrderEntity:
        order = self._order_repo.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(
                _("Orden %(order_id)s no encontrada.")
                % {"order_id": order_id}
            )
        return order

    def _queue_order_event(self, order_id: int, event: str) -> None:
        try:
            send_order_notification.delay(order_id, event)
        except Exception:
            logger.warning(
                "No se pudo encolar la notificacion %s para el pedido %s.",
                event,
                order_id,
                exc_info=True,
            )

    def _queue_daily_report(self, delivery_date: str) -> None:
        if not delivery_date:
            return
        try:
            build_daily_order_report.delay(delivery_date)
        except Exception:
            logger.warning(
                "No se pudo encolar el reporte diario para %s.",
                delivery_date,
                exc_info=True,
            )
