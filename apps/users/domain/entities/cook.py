from django.utils.translation import gettext_lazy as _


class CookProfile:
    def __init__(self, name: str, specialty: str):
        self.name = self._validate_name(name)
        self.specialty = self._validate_specialty(specialty)

    def _validate_name(self, value: str) -> str:
        if not value or not value.strip():
            raise ValueError(_("name no puede estar vacío"))
        return value.strip()

    def _validate_specialty(self, value: str) -> str:
        if not value or not value.strip():
            raise ValueError(_("specialty no puede estar vacío"))
        return value.strip()

    def change_specialty(self, new_specialty: str):
        self.specialty = self._validate_specialty(new_specialty)

    def __repr__(self):
        return f"<CookProfile {self.name} - {self.specialty}>"
