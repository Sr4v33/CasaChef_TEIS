from apps.dishes.domain.entities.product import ProductEntity
from apps.dishes.infrastructure.models.product_model import ProductModel


class ProductMapper:
    @staticmethod
    def to_domain(model: ProductModel) -> ProductEntity:
        return ProductEntity(
            product_id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            stock=model.stock,
        )

    @staticmethod
    def to_model(entity: ProductEntity) -> dict:
        return {
            "id": entity.product_id,
            "name": entity.name,
            "description": entity.description,
            "price": entity.price,
            "stock": entity.stock,
        }
