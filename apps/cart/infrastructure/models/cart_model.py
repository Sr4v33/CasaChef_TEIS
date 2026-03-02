import uuid
from django.db import models
from django.conf import settings


class CartModel(models.Model):
    """Persistencia de Cart (Django ORM).

    Un cliente tiene máximo un carrito activo (OneToOne con User).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Referencia al usuario propietario del carrito.
    # Usamos settings.AUTH_USER_MODEL para compatibilidad con el User de Django.
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "cart"

    def __str__(self) -> str:
        return f"Cart {self.id} (customer={self.customer_id})" # type: ignore[attr-defined]