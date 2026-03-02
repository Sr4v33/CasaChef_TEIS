from apps.cart.domain.entities.cart import CartEntity
from apps.cart.domain.entities.cart_item import CartItemEntity
from apps.cart.infrastructure.models.cart_model import CartModel
from apps.cart.infrastructure.models.cart_item_model import CartItemModel


class CartMapper:
    """Traduce entre entidades de dominio y modelos de Django ORM.

    Separa el dominio de la infraestructura: la entidad Cart no sabe nada
    de Django, y el modelo CartModel no tiene lógica de negocio.
    """

    @staticmethod
    def to_domain(model: CartModel) -> CartEntity:
        cart = CartEntity(
            customer_id=model.customer_id, # type: ignore[attr-defined]
            cart_id=model.id,
        )
        # Reconstruir los ítems desde la base de datos
        for item_model in model.items.all(): # type: ignore[attr-defined]
            cart._items[item_model.product_id] = CartItemMapper.to_domain(item_model)
        return cart

    @staticmethod
    def to_model_dict(entity: CartEntity) -> dict:
        return {
            "id": entity.cart_id,
            "customer_id": entity.customer_id,
        }


class CartItemMapper:
    @staticmethod
    def to_domain(model: CartItemModel) -> CartItemEntity:
        return CartItemEntity(
            cart_item_id=model.id,
            product_id=model.product_id,
            quantity=model.quantity,
            unit_price=model.unit_price,
        )

    @staticmethod
    def to_model_dict(entity: CartItemEntity, cart_id) -> dict:
        return {
            "id": entity.cart_item_id,
            "cart_id": cart_id,
            "product_id": entity.product_id,
            "quantity": entity.quantity,
            "unit_price": entity.unit_price,
        }