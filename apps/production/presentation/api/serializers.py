from rest_framework import serializers


# ─── Input Serializers ────────────────────────────────────────────────────────

class CreateProductionSerializer(serializers.Serializer):
    """Valida la entrada para crear un registro de producción diaria."""
    dish_id         = serializers.IntegerField(min_value=1)
    date            = serializers.DateField()
    available_units = serializers.IntegerField(min_value=0)


class AdjustUnitsSerializer(serializers.Serializer):
    """Valida el ajuste de cupos disponibles."""
    available_units = serializers.IntegerField(min_value=0)


# ─── Output Serializers ───────────────────────────────────────────────────────

class ProductionOutputSerializer(serializers.Serializer):
    """Serializa una DailyProductionEntity para la respuesta."""
    production_id   = serializers.IntegerField()
    dish_id         = serializers.IntegerField()
    date            = serializers.CharField()
    available_units = serializers.IntegerField()
