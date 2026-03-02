from rest_framework import serializers


# ─── Input Serializers ────────────────────────────────────────────────────────

class OrderItemInputSerializer(serializers.Serializer):
    """Ítem individual dentro de la creación de una orden."""

    dish_id    = serializers.IntegerField(min_value=1)
    quantity   = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)


class CreateOrderSerializer(serializers.Serializer):
    """Valida el body de POST /api/orders/."""

    items   = OrderItemInputSerializer(many=True, min_length=1)
    address = serializers.CharField(max_length=500)
    date    = serializers.DateField()                  # YYYY-MM-DD


# ─── Output Serializers ───────────────────────────────────────────────────────

class OrderItemOutputSerializer(serializers.Serializer):
    dish_id    = serializers.IntegerField()
    quantity   = serializers.IntegerField()
    unit_price = serializers.FloatField()


class OrderOutputSerializer(serializers.Serializer):
    """Serializa un OrderEntity para la respuesta."""

    order_id     = serializers.IntegerField()
    user_id      = serializers.IntegerField()
    address      = serializers.CharField()
    date         = serializers.CharField()
    status       = serializers.CharField()
    items        = OrderItemOutputSerializer(many=True)
    total        = serializers.SerializerMethodField()

    def get_total(self, obj) -> float:
        return obj.calculate_total()