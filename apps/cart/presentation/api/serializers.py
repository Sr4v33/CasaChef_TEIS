from decimal import Decimal
from rest_framework import serializers


class AddProductSerializer(serializers.Serializer):
    """Valida la entrada para añadir un producto al carrito."""

    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal("0"))


class RemoveProductSerializer(serializers.Serializer):
    """Valida la entrada para eliminar un producto del carrito."""

    product_id = serializers.UUIDField()


class CartItemOutputSerializer(serializers.Serializer):
    """Serializa un CartItem para la respuesta."""

    cart_item_id = serializers.UUIDField()
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    subtotal = serializers.SerializerMethodField()

    def get_subtotal(self, obj) -> Decimal:
        return obj.calculate_subtotal()


class CartOutputSerializer(serializers.Serializer):
    """Serializa el Cart completo para la respuesta."""

    cart_id = serializers.UUIDField()
    customer_id = serializers.UUIDField()
    items = CartItemOutputSerializer(many=True)
    total = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()

    def get_total(self, obj) -> Decimal:
        return obj.calculate_total()

    def get_item_count(self, obj) -> int:
        return obj.item_count()