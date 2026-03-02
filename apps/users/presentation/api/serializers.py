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


# ─── Output Serializers ───────────────────────────────────────────────────────

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