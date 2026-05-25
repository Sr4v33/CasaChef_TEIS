import uuid
from typing import Optional, List
from django.utils.translation import gettext_lazy as _

from .address import Address
from .customer import CustomerProfile
from .cook import CookProfile


class User:
    def __init__(
        self,
        email: str,
        active: bool = True,
        user_id: uuid.UUID | None = None,
        customer_profile: Optional[CustomerProfile] = None,
        cook_profile: Optional[CookProfile] = None,
        addresses: Optional[List[Address]] = None
    ):
        self.id = user_id or uuid.uuid4()
        self.email = self._validate_email(email)
        self.active = active

        self.customer_profile = customer_profile
        self.cook_profile = cook_profile
        self.addresses = addresses or []

    # Estados del usuario

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    # Validación de Email

    def _validate_email(self, value: str) -> str:
        if not value or "@" not in value:
            raise ValueError(_("Correo electrónico inválido"))
        return value.strip().lower()

    # Rol del usuario

    def add_customer_profile(self, profile: CustomerProfile):
        if self.customer_profile:
            raise ValueError(_("El usuario ya tiene un perfil de cliente"))
        self.customer_profile = profile

    def add_cook_profile(self, profile: CookProfile):
        if self.cook_profile:
            raise ValueError(_("El usuario ya tiene un perfil de cocinero"))
        self.cook_profile = profile

    def is_customer(self) -> bool:
        return self.customer_profile is not None

    def is_cook(self) -> bool:
        return self.cook_profile is not None

    # Direcciones

    def add_address(self, address: Address):
        if address.is_default:
            self._unset_existing_default()
        self.addresses.append(address)

    def _unset_existing_default(self):
        for addr in self.addresses:
            if addr.is_default:
                addr.unset_default()

    def get_default_address(self) -> Optional[Address]:
        for addr in self.addresses:
            if addr.is_default:
                return addr
        return None

    def __repr__(self):
        return f"<User {self.email}>"
