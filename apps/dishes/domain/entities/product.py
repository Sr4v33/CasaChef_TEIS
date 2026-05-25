from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Optional
from django.utils.translation import gettext_lazy as _

from ..exceptions import InvalidProductData, InsufficientStock
from ..ports.discount_policy_port import DiscountPolicyPort


def _as_decimal(value: Any, field_name: str) -> Decimal:
    try:
        d = value if isinstance(value, Decimal) else Decimal(str(value))
    except Exception as exc:  # pragma: no cover
        raise InvalidProductData(
            _("%(field_name)s debe ser numérico") % {"field_name": field_name}
        ) from exc
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
            raise InvalidProductData(_("price no puede ser negativo"))

        if not isinstance(self.stock, int) or self.stock < 0:
            raise InvalidProductData(_("stock debe ser un entero >= 0"))

    # -----------------------------
    # Métodos de negocio (UML)
    # -----------------------------

    def validate_stock(self, quantity: int) -> None:
        """Valida que haya stock suficiente para una cantidad dada."""
        if not isinstance(quantity, int) or quantity <= 0:
            raise InvalidProductData(_("Cantidad debe ser un entero mayor a 0"))

        if quantity > self.stock:
            raise InsufficientStock(
                _(
                    "Stock insuficiente para '%(product_name)s'. "
                    "Disponible=%(available)s, solicitado=%(requested)s"
                )
                % {
                    "product_name": self.name,
                    "available": self.stock,
                    "requested": quantity,
                }
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
            raise InvalidProductData(_("El descuento no puede ser negativo"))

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
            raise InvalidProductData(
                _("%(field_name)s no puede estar vacío")
                % {"field_name": field_name}
            )
        return value.strip()


# Alias para compatibilidad con otros módulos
ProductEntity = Product
