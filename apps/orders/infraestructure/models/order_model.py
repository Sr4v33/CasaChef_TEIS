from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = (
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    address = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CONFIRMED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user}" # type: ignore