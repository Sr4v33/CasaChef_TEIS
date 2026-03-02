from django.db import models
from django.conf import settings


class AddressModel(models.Model):
    """Modelo de infraestructura para Address.

    FK al User de Django (AUTH_USER_MODEL) para permitir gestión de direcciones
    directamente desde el usuario autenticado en las vistas.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    street     = models.CharField(max_length=255)
    city       = models.CharField(max_length=100)
    state      = models.CharField(max_length=100)
    zip_code   = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    class Meta:
        app_label = "users"

    def __str__(self):
        return f"{self.street}, {self.city}"
