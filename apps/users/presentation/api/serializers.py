from rest_framework import serializers


# ─── Input Serializers ────────────────────────────────────────────────────────

class RegisterUserSerializer(serializers.Serializer):
    """Valida la entrada para registrar un usuario nuevo."""
    email    = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)


class CustomerProfileSerializer(serializers.Serializer):
    """Valida los datos del perfil de cliente."""
    full_name = serializers.CharField(max_length=200)
    phone     = serializers.CharField(min_length=7, max_length=20)


class CookProfileSerializer(serializers.Serializer):
    """Valida los datos del perfil de cocinero."""
    name      = serializers.CharField(max_length=200)
    specialty = serializers.CharField(max_length=200)


class AddressSerializer(serializers.Serializer):
    """Valida la entrada para crear una dirección."""
    street     = serializers.CharField(max_length=255)
    city       = serializers.CharField(max_length=100)
    state      = serializers.CharField(max_length=100)
    zip_code   = serializers.CharField(max_length=20)
    is_default = serializers.BooleanField(default=False)


# ─── Output Serializers ───────────────────────────────────────────────────────

class AddressOutputSerializer(serializers.Serializer):
    address_id = serializers.UUIDField(source="id")
    street     = serializers.CharField()
    city       = serializers.CharField()
    state      = serializers.CharField()
    zip_code   = serializers.CharField()
    is_default = serializers.BooleanField()


class CustomerProfileOutputSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    phone     = serializers.CharField()


class CookProfileOutputSerializer(serializers.Serializer):
    name      = serializers.CharField()
    specialty = serializers.CharField()


class UserOutputSerializer(serializers.Serializer):
    """Serializa un UserEntity para la respuesta."""
    user_id          = serializers.UUIDField(source="id")
    email            = serializers.EmailField()
    active           = serializers.BooleanField()
    customer_profile = CustomerProfileOutputSerializer(allow_null=True)
    cook_profile     = CookProfileOutputSerializer(allow_null=True)
