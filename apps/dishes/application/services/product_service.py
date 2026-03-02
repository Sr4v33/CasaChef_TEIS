from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from apps.dishes.domain.entities.product import ProductEntity
from apps.dishes.domain.ports.discount_policy_port import DiscountPolicyPort
from apps.dishes.domain.ports.product_repository_port import ProductRepositoryPort


class ProductService:
    """Service Layer para casos de uso de Product.

    Expone métodos públicos para todos los casos de uso. Ninguna vista debe
    acceder a _repo directamente: toda consulta pasa por este servicio.
    """

    def __init__(self, repo: ProductRepositoryPort) -> None:
        self._repo = repo

    def register_product(
        self,
        *,
        name: str,
        description: str,
        price: Decimal,
        stock: int,
    ) -> ProductEntity:
        """Crea y persiste un nuevo producto en el catálogo."""
        product = ProductEntity(
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
        return self._repo.save(product)

    def get_product(self, product_id: UUID) -> Optional[ProductEntity]:
        """Retorna un producto por su UUID o None si no existe.

        Las vistas deben usar este método en lugar de acceder a _repo directamente.
        """
        return self._repo.get_by_id(product_id)

    def get_product_by_name(self, name: str) -> Optional[ProductEntity]:
        """Retorna un producto por su nombre o None si no existe."""
        return self._repo.get_by_name(name)

    def price_after_discount(
        self,
        product: ProductEntity,
        *,
        customer: Any | None = None,
        policy: Optional[DiscountPolicyPort] = None,
    ) -> Decimal:
        """Calcula el precio final aplicando el descuento correspondiente."""
        return product.price - product.calculate_discount(customer, policy=policy)