from django.db import models
from django.conf import settings
from .order_model import Order

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    dish_id = models.PositiveIntegerField()

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Item {self.dish_id} x {self.quantity}"
