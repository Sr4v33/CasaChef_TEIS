class CustomerProfile:
    def __init__(self, full_name: str, phone: str):
        self.full_name = self._validate_name(full_name)
        self.phone = self._validate_phone(phone)

    def _validate_name(self, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("full_name cannot be empty")
        return value.strip()

    def _validate_phone(self, value: str) -> str:
        if not value or len(value.strip()) < 7:
            raise ValueError("Invalid phone number")
        return value.strip()

    def update_phone(self, new_phone: str):
        self.phone = self._validate_phone(new_phone)

    def __repr__(self):
        return f"<CustomerProfile {self.full_name}>"