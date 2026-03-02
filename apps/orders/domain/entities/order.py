from dataclasses import dataclass, field
from typing import List

from apps.orders.domain.entities.order_item import OrderItemEntity
from apps.orders.domain.exceptions import InvalidOrderTransition


@dataclass
class OrderEntity:
    """Entidad de dominio Order.

    Contiene los métodos de negocio del ciclo de vida del pedido
    (confirm, cancel) que el UML define como confirm() y cancel().
    La lógica de transición de estado vive aquí, no en el service.
    """

    user_id: int
    address: str
    date: str
    items: List[OrderItemEntity]
    status: str = "PENDING"
    order_id: int = 0           # poblado por el repositorio tras persistir
    order_number: str = ""

    # ------------------------------------------
    # Métodos de negocio — ciclo de vida (UML)
    # ------------------------------------------

    def confirm(self) -> None:
        """Confirma la orden. Solo es válido desde estado PENDING."""
        if self.status != "PENDING":
            raise InvalidOrderTransition(
                f"No se puede confirmar una orden en estado '{self.status}'"
            )
        self.status = "CONFIRMED"

    def cancel(self) -> None:
        """Cancela la orden. Válido desde PENDING o CONFIRMED."""
        if self.status == "CANCELLED":
            raise InvalidOrderTransition("La orden ya está cancelada")
        self.status = "CANCELLED"

    # ------------------------------------------
    # Cálculos (no mutan estado)
    # ------------------------------------------

    def calculate_total(self) -> float:
        return sum(i.quantity * i.unit_price for i in self.items)