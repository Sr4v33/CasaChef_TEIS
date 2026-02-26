from decimal import Decimal
from typing import Any, Optional

from apps.dishes.domain.entities.product import ProductEntity
from apps.dishes.domain.ports.discount_policy_port import DiscountPolicyPort
from apps.dishes.domain.ports.product_repository_port import ProductRepositoryPort


class ProductService:
    """Service Layer para casos de uso de Product.

    El Service Layer mejora testabilidad/portabilidad (la lógica vive fuera de la vista
    y sin requerir infraestructura real).
    """

    def __init__(self, repo: ProductRepositoryPort):
        self._repo = repo

    def register_product(self, *, name: str, description: str, price: Decimal, stock: int) -> ProductEntity:
        product = ProductEntity(name=name, description=description, price=price, stock=stock)
        return self._repo.save(product)

    # Revisar metodo!!
    def price_after_discount(
        self,
        product: ProductEntity,
        *,
        customer: Any | None = None,
        policy: Optional[DiscountPolicyPort] = None,
    ) -> Decimal:
        return product.price - product.calculate_discount(customer, policy=policy) # Revisar!!
