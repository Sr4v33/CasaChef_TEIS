from typing import Optional
from uuid import UUID

from apps.dishes.domain.entities.product import ProductEntity
from apps.dishes.domain.ports.product_repository_port import ProductRepositoryPort
from apps.dishes.infrastructure.mappers.product_mapper import ProductMapper
from apps.dishes.infrastructure.models.product_model import ProductModel


class DjangoProductRepository(ProductRepositoryPort):
    def save(self, product: ProductEntity) -> ProductEntity:
        ProductModel.objects.update_or_create(
            id=product.product_id,
            defaults=ProductMapper.to_model(product),
        )
        return product

    def get_by_id(self, product_id: UUID) -> Optional[ProductEntity]:
        try:
            m = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return None
        return ProductMapper.to_domain(m)

    def get_by_name(self, name: str) -> Optional[ProductEntity]:
        try:
            m = ProductModel.objects.get(name=name)
        except ProductModel.DoesNotExist:
            return None
        return ProductMapper.to_domain(m)
