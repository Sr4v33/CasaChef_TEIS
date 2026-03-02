from typing import Optional
from uuid import UUID

from django.db import transaction

from apps.cart.domain.entities.cart import CartEntity
from apps.cart.domain.ports.cart_repository_port import CartRepositoryPort
from apps.cart.infrastructure.mappers.cart_mapper import CartMapper, CartItemMapper
from apps.cart.infrastructure.models.cart_model import CartModel
from apps.cart.infrastructure.models.cart_item_model import CartItemModel


class DjangoCartRepository(CartRepositoryPort):
    """Implementación con Django ORM del repositorio de Cart.

    Sigue el patrón Repository: la capa de aplicación solo conoce la interfaz
    CartRepositoryPort; esta clase concreta vive en infraestructura.
    """

    @transaction.atomic
    def save(self, cart: CartEntity) -> CartEntity:
        # Persistir (o actualizar) el carrito
        cart_model, _ = CartModel.objects.update_or_create(
            id=cart.cart_id,
            defaults={"customer_id": cart.customer_id},
        )

        # Sincronizar ítems: borrar los que ya no existen y crear/actualizar los actuales
        current_product_ids = {item.product_id for item in cart.items}

        # Eliminar ítems que fueron removidos del carrito
        CartItemModel.objects.filter(cart=cart_model).exclude(
            product_id__in=current_product_ids
        ).delete()

        # Crear o actualizar los ítems actuales
        for item in cart.items:
            CartItemModel.objects.update_or_create(
                cart=cart_model,
                product_id=item.product_id,
                defaults={
                    "id": item.cart_item_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                },
            )

        return cart

    def get_by_id(self, cart_id: UUID) -> Optional[CartEntity]:
        try:
            model = CartModel.objects.prefetch_related("items").get(id=cart_id)
        except CartModel.DoesNotExist:
            return None
        return CartMapper.to_domain(model)

    def get_by_customer_id(self, customer_id: UUID) -> Optional[CartEntity]:
        try:
            model = CartModel.objects.prefetch_related("items").get(
                customer_id=customer_id
            )
        except CartModel.DoesNotExist:
            return None
        return CartMapper.to_domain(model)

    @transaction.atomic
    def delete(self, cart_id: UUID) -> None:
        CartModel.objects.filter(id=cart_id).delete()