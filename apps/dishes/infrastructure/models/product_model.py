from django.db import models


class ProductModel(models.Model):
    """Persistencia del Product (Django ORM).

    Nota: mantenemos el modelo en infraestructura para separar Dominio de Framework.
    """

    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} (${self.price})"
