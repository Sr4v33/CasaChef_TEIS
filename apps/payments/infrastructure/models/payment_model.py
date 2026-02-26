from django.db import models


class PaymentModel(models.Model):
    """Persistencia de Payment.

    Nota: dejamos `order_id` como IntegerField para evitar dependencia directa con el
    modelo de Order mientras el módulo orders se estabiliza.
    Si luego existe un Order model registrado por Django, cambia a:
        order = models.OneToOneField('orders.Order', on_delete=models.PROTECT, related_name='payment')
    """

    id = models.UUIDField(primary_key=True)

    # Aquí iría el FK/OneToOne a Order según el UML (paidBy 1..1)
    order_id = models.PositiveIntegerField(null=True, blank=True)

    METHOD_CHOICES = (
        ("CARD", "Card"),
        ("BANK_TRANSFER", "Bank Transfer"),
        ("CASH", "Cash"),
    )
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("FAILED", "Failed"),
    )

    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    transaction_reference = models.CharField(max_length=200, null=True, blank=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="COP")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["order_id"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"Payment {self.id} ({self.status})"
