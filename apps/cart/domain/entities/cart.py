from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Optional

from ..exceptions import (
    CartIsEmptyError,
    InvalidCartItemData,
    ProductAlreadyInCartError,
    ProductNotInCartError,
)
from .cart_item import CartItem


@dataclass
class Cart:
    """Entidad de dominio Cart.

    Pertenece a un Customer (owns 1:1 en el UML).
    Contiene CartItems (1..* composición) y es la raíz agregada
    del proceso de compra antes de convertirse en Order.

    Reglas de negocio encapsuladas:
    - No se puede añadir el mismo producto dos veces (se actualiza la cantidad).
    - El total se calcula a partir de los ítems (no se almacena como estado mutable).
    - validate_availability delega en un puerto para no acoplar el dominio a infraestructura.
    """

    customer_id: uuid.UUID
    cart_id: uuid.UUID = field(default_factory=uuid.uuid4)

    # Mapa product_id → CartItem para búsqueda O(1)
    _items: Dict[uuid.UUID, CartItem] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.customer_id, uuid.UUID):
            try:
                self.customer_id = uuid.UUID(str(self.customer_id))
            except Exception as exc:
                raise InvalidCartItemData("customer_id debe ser un UUID válido") from exc

    # -------------------------
    # Métodos de negocio (UML)
    # -------------------------

    def add_product(self, product_id: uuid.UUID, quantity: int, unit_price: Decimal) -> CartItem:
        """Añade un producto al carrito.

        Si el producto ya existe, suma la cantidad (no duplica el ítem).
        Esto refleja el comportamiento esperado en un carrito de compras real.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise InvalidCartItemData("quantity debe ser un entero mayor a 0")

        if product_id in self._items:
            # Acumular cantidad en lugar de rechazar (UX esperada)
            existing = self._items[product_id]
            existing.update_quantity(existing.quantity + quantity)
            return existing

        item = CartItem(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        self._items[product_id] = item
        return item

    def remove_product(self, product_id: uuid.UUID) -> None:
        """Elimina un producto del carrito.

        Lanza ProductNotInCartError si el producto no existe.
        """
        if product_id not in self._items:
            raise ProductNotInCartError(
                f"El producto {product_id} no está en el carrito"
            )
        del self._items[product_id]

    def calculate_total(self) -> Decimal:
        """Calcula el total sumando los subtotales de todos los ítems."""
        return sum(
            (item.calculate_subtotal() for item in self._items.values()),
            Decimal("0"),
        )

    def validate_availability(self, stock_checker) -> None:
        """Verifica que todos los productos del carrito tengan stock disponible.

        Recibe un callable/port que encapsula la lógica de consulta de stock,
        cumpliendo con DIP: el dominio no depende de infraestructura concreta.

        Args:
            stock_checker: objeto con método `check(product_id, quantity) -> bool`
        """
        if self.is_empty():
            raise CartIsEmptyError("El carrito está vacío")

        for item in self._items.values():
            stock_checker.check(
                product_id=item.product_id,
                quantity=item.quantity,
            )

    # -------------------------
    # Consultas / helpers
    # -------------------------

    def get_item(self, product_id: uuid.UUID) -> Optional[CartItem]:
        return self._items.get(product_id)

    @property
    def items(self) -> List[CartItem]:
        """Lista inmutable de ítems del carrito."""
        return list(self._items.values())

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def item_count(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        """Vacía el carrito (útil tras confirmar el pedido)."""
        self._items.clear()

    def __repr__(self) -> str:
        return (
            f"<Cart cart_id={self.cart_id} "
            f"customer_id={self.customer_id} "
            f"items={self.item_count()} "
            f"total={self.calculate_total()}>"
        )


# Alias para compatibilidad
CartEntity = Cart