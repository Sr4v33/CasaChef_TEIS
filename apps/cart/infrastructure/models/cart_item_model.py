import uuid
from django.db import models
from .cart_model import CartModel


class CartItemModel(models.Model):
    """Persistencia de CartItem (Django ORM).

    Composición con Cart: si se elimina el Cart, se eliminan sus ítems.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    cart = models.ForeignKey(
        CartModel,
        on_delete=models.CASCADE,
        related_name="items",
    )

    # UUID del producto referenciado (desacoplado del modelo ProductModel
    # para evitar FK cruzada entre apps; la integridad se valida en el dominio).
    product_id = models.UUIDField()

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        app_label = "cart"
        # Un producto no puede repetirse dentro del mismo carrito
        unique_together = ("cart", "product_id")

    def __str__(self) -> str:
        return f"CartItem product={self.product_id} qty={self.quantity}"