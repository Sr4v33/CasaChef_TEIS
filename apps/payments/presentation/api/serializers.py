from rest_framework import serializers
from apps.payments.domain.entities.payment import PaymentMethod


# ─── Input Serializers ────────────────────────────────────────────────────────

class PayOrderSerializer(serializers.Serializer):
    """Valida la entrada para procesar el pago de una orden."""

    order_id = serializers.IntegerField(min_value=1)
    amount   = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    method   = serializers.ChoiceField(choices=[m.value for m in PaymentMethod])


# ─── Output Serializers ───────────────────────────────────────────────────────

class PaymentOutputSerializer(serializers.Serializer):
    """Serializa un PaymentEntity para la respuesta."""

    payment_id            = serializers.UUIDField()
    method                = serializers.CharField()
    status                = serializers.CharField()
    transaction_reference = serializers.CharField(allow_null=True)