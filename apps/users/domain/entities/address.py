import uuid
from django.utils.translation import gettext_lazy as _

class Address:
    def __init__(
        self,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        is_default: bool = False,
        address_id: uuid.UUID | None = None
    ):
        self.id = address_id or uuid.uuid4()
        self.street = self._validate_non_empty(street, "street")
        self.city = self._validate_non_empty(city, "city")
        self.state = self._validate_non_empty(state, "state")
        self.zip_code = self._validate_non_empty(zip_code, "zip_code")
        self.is_default = is_default

    def set_as_default(self):
        self.is_default = True

    def unset_default(self):
        self.is_default = False

    def _validate_non_empty(self, value: str, field_name: str) -> str:
        if not value or not value.strip():
            raise ValueError(
                _("%(field_name)s no puede estar vacío")
                % {"field_name": field_name}
            )
        return value.strip()

    def __repr__(self):
        return f"<Address {self.street}, {self.city}>"
