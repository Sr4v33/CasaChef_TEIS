from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Optional

from ..exceptions import InvalidProductData, InsufficientStock
from ..ports.discount_policy_port import DiscountPolicyPort


def _as_decimal(value: Any, field_name: str) -> Decimal:
    try:
        d = value if isinstance(value, Decimal) else Decimal(str(value))
    except Exception as exc:  # pragma: no cover
        raise InvalidProductData(f"{field_name} debe ser numérico") from exc
    return d


@dataclass(slots=True)
class Product:
    """Entidad de dominio Product.

    Encapsula reglas de negocio como `validate_stock()` y `calculate_discount()`.
    """

    name: str
    description: str
    price: Decimal
    stock: int

    product_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self) -> None:
        self.name = self._validate_non_empty(self.name, "name")
        self.description = (self.description or "").strip()
        self.price = _as_decimal(self.price, "price")
        if self.price < 0:
            raise InvalidProductData("price no puede ser negativo")

        if not isinstance(self.stock, int) or self.stock < 0:
            raise InvalidProductData("stock debe ser un entero >= 0")

    # -----------------------------
    # Métodos de negocio (UML)
    # -----------------------------

    def validate_stock(self, quantity: int) -> None:
        """Valida que haya stock suficiente para una cantidad dada."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise InvalidProductData("Cantidad debe ser un entero mayor a 0")

        if quantity > self.stock:
            raise InsufficientStock(
                f"Stock insuficiente para '{self.name}'. "
                f"Disponible={self.stock}, solicitado={quantity}"
            )

    def calculate_discount(
        self,
        customer: Any | None = None,
        *,
        policy: Optional[DiscountPolicyPort] = None,
    ) -> Decimal:
        """Calcula el descuento (en dinero) aplicable a este producto.

        Sigue OCP/SRP: la regla de descuento vive en la Policy (Strategy),
        no en la entidad. Para agregar nuevas reglas basta con implementar
        DiscountPolicyPort sin modificar Product.
        """
        if policy is None:
            return Decimal("0")

        # La regla de descuento vive en la política, no en la entidad (SRP/OCP)
        discount = policy.get_discount_amount(product=self, customer=customer)

        discount = _as_decimal(discount, "discount")
        if discount < 0:
            raise InvalidProductData("El descuento no puede ser negativo")

        # El descuento no puede superar el precio del producto
        return min(discount, self.price)

    def update_stock(self, quantity: int) -> None:
        """Descuenta stock después de una venta/reserva."""
        self.validate_stock(quantity)
        self.stock -= quantity

    # -----------------------------
    # Helpers
    # -----------------------------

    def _validate_non_empty(self, value: str, field_name: str) -> str:
        if not value or not value.strip():
            raise InvalidProductData(f"{field_name} no puede estar vacío")
        return value.strip()


# Alias para compatibilidad con otros módulos
ProductEntity = Product