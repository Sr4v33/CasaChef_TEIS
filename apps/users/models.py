# Django autodiscovery shim for clean-architecture models.
# Importar los modelos de infraestructura para que Django los registre
# y pueda generar/aplicar migraciones correctamente.
from apps.users.infrastructure.models.user_model import UserModel
from apps.users.infrastructure.models.customer_model import CustomerModel
from apps.users.infrastructure.models.cook_model import CookModel
from apps.users.infrastructure.models.address_model import AddressModel

__all__ = ["UserModel", "CustomerModel", "CookModel", "AddressModel"]
