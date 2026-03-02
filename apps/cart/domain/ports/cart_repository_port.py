from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.cart import CartEntity


class CartRepositoryPort(ABC):
    """Contrato de persistencia para Cart."""

    @abstractmethod
    def save(self, cart: CartEntity) -> CartEntity:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, cart_id: UUID) -> Optional[CartEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_customer_id(self, customer_id: UUID) -> Optional[CartEntity]:
        """Retorna el carrito activo de un customer, o None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, cart_id: UUID) -> None:
        """Elimina el carrito (tras conversión a Order, por ejemplo)."""
        raise NotImplementedError