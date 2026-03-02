from typing import cast, Dict, Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.production.application.services.production_service import ProductionService
from apps.production.infrastructure.repositories.django_production_repository import DjangoProductionRepository
from apps.production.presentation.api.serializers import (
    CreateProductionSerializer,
    AdjustUnitsSerializer,
    ProductionOutputSerializer,
)


def _build_service() -> ProductionService:
    return ProductionService(repo=DjangoProductionRepository())


class ProductionListCreateView(APIView):
    """
    GET  /api/production/          — Lista registros de producción (filtrable por dish_id y date).
    POST /api/production/          — Crea un nuevo registro de producción diaria.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        dish_id = request.query_params.get("dish_id")
        date = request.query_params.get("date")

        service = _build_service()
        productions = service.list_productions(
            dish_id=int(dish_id) if dish_id else None,
            date=date,
        )
        return Response(
            ProductionOutputSerializer(productions, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CreateProductionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            production = service.create_production(
                dish_id=data["dish_id"],
                date=str(data["date"]),
                available_units=data["available_units"],
            )
        except ValueError as exc:
            # 409: ya existe un registro para ese plato y fecha
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(
            ProductionOutputSerializer(production).data,
            status=status.HTTP_201_CREATED,
        )


class ProductionDetailView(APIView):
    """
    GET   /api/production/<id>/   — Consulta cupos disponibles para un plato y fecha.
    PATCH /api/production/<id>/   — Ajusta los cupos disponibles del día.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, production_id: int):
        service = _build_service()
        production = service.get_production(production_id)
        if production is None:
            return Response(
                {"error": "Registro de producción no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            ProductionOutputSerializer(production).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, production_id: int):
        serializer = AdjustUnitsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            production = service.adjust_units(
                production_id=production_id,
                new_units=data["available_units"],
            )
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            ProductionOutputSerializer(production).data,
            status=status.HTTP_200_OK,
        )
