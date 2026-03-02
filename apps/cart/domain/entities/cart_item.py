from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from ..exceptions import InvalidCartItemData


def _as_decimal(value: Any, field_name: str) -> Decimal:
    try:
        return value if isinstance(value, Decimal) else Decimal(str(value))
    except Exception as exc:
        raise InvalidCartItemData(f"{field_name} debe ser numérico") from exc


@dataclass
class CartItem:
    """Entidad de dominio CartItem.

    Representa un producto dentro del carrito con su cantidad y precio unitario.
    El precio unitario se fija en el momento de añadir al carrito (snapshot de precio),
    evitando inconsistencias si el producto cambia de precio antes del checkout.
    """

    product_id: uuid.UUID
    quantity: int
    unit_price: Decimal

    cart_item_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self) -> None:
        if not isinstance(self.product_id, uuid.UUID):
            try:
                self.product_id = uuid.UUID(str(self.product_id))
            except Exception as exc:
                raise InvalidCartItemData("product_id debe ser un UUID válido") from exc

        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise InvalidCartItemData("quantity debe ser un entero mayor a 0")

        self.unit_price = _as_decimal(self.unit_price, "unit_price")
        if self.unit_price < 0:
            raise InvalidCartItemData("unit_price no puede ser negativo")

    # -------------------------
    # Métodos de negocio (UML)
    # -------------------------

    def calculate_subtotal(self) -> Decimal:
        """Retorna el subtotal del ítem (quantity × unit_price)."""
        return self.quantity * self.unit_price

    def update_quantity(self, new_quantity: int) -> None:
        """Actualiza la cantidad del ítem con validación."""
        if not isinstance(new_quantity, int) or new_quantity <= 0:
            raise InvalidCartItemData("La nueva cantidad debe ser un entero mayor a 0")
        self.quantity = new_quantity

    def __repr__(self) -> str:
        return (
            f"<CartItem product_id={self.product_id} "
            f"qty={self.quantity} unit_price={self.unit_price}>"
        )


# Alias para compatibilidad
CartItemEntity = CartItem