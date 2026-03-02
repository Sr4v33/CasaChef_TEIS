from decimal import Decimal
from rest_framework import serializers


# ─── Input Serializers ────────────────────────────────────────────────────────

class RegisterProductSerializer(serializers.Serializer):
    """Valida la entrada para registrar (crear/actualizar) un producto."""

    name        = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    price       = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal("0.01"))
    stock       = serializers.IntegerField(min_value=0)


# ─── Output Serializers ───────────────────────────────────────────────────────

class ProductOutputSerializer(serializers.Serializer):
    """Serializa un ProductEntity para la respuesta."""

    product_id  = serializers.UUIDField()
    name        = serializers.CharField()
    description = serializers.CharField()
    price       = serializers.DecimalField(max_digits=12, decimal_places=2)
    stock       = serializers.IntegerField()