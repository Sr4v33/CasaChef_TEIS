from typing import Optional, Union
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

    NOTA: CartModel.customer es FK al User de Django (clave primaria entera).
    Las vistas pasan request.user.id (int) como customer_id, por lo que el
    repositorio usa ese valor directamente para la FK, sin conversión a UUID.
    """

    @transaction.atomic
    def save(self, cart: CartEntity) -> CartEntity:
        # customer_id puede ser int (PK de Django) o UUID — normalizamos a int si es necesario
        customer_pk = self._resolve_customer_pk(cart.customer_id)

        cart_model, _ = CartModel.objects.update_or_create(
            id=cart.cart_id,
            defaults={"customer_id": customer_pk},
        )

        current_product_ids = {item.product_id for item in cart.items}

        CartItemModel.objects.filter(cart=cart_model).exclude(
            product_id__in=current_product_ids
        ).delete()

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

    def get_by_customer_id(self, customer_id) -> Optional[CartEntity]:
        customer_pk = self._resolve_customer_pk(customer_id)
        try:
            model = CartModel.objects.prefetch_related("items").get(
                customer_id=customer_pk
            )
        except CartModel.DoesNotExist:
            return None
        return CartMapper.to_domain(model)

    @transaction.atomic
    def delete(self, cart_id: UUID) -> None:
        CartModel.objects.filter(id=cart_id).delete()

    # ------------------------------------------------------------------
    # Helper: acepta tanto int (PK Django) como UUID de dominio
    # ------------------------------------------------------------------
    @staticmethod
    def _resolve_customer_pk(customer_id) -> int:
        """Devuelve el PK entero del User de Django.

        Si customer_id ya es un entero (o un string numérico) lo devuelve tal cual.
        Los UUID de dominio llegan cuando el carrito viene del mapper; en ese caso
        necesitamos buscar el User por UUID o asumir que el valor es el PK directo.
        """
        if isinstance(customer_id, int):
            return customer_id
        try:
            return int(customer_id)
        except (ValueError, TypeError):
            # UUID de dominio — buscar el User de Django cuyo campo pk coincida
            # En la práctica las vistas siempre pasan request.user.id (int),
            # por lo que este caso es solo un fallback de seguridad.
            from django.contrib.auth import get_user_model
            User = get_user_model()
            # Intentar buscar por UUID si el campo existe
            try:
                user = User.objects.get(id=str(customer_id))
                return user.pk
            except User.DoesNotExist:
                raise ValueError(
                    f"No se encontró un usuario con id={customer_id}"
                )
