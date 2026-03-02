from typing import cast, Dict, Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.dishes.application.services.product_service import ProductService
from apps.dishes.domain.exceptions import InvalidProductData, InsufficientStock
from apps.dishes.infrastructure.repositories.django_product_repository import DjangoProductRepository
from apps.dishes.presentation.api.serializers import (
    RegisterProductSerializer,
    ProductOutputSerializer,
)


def _build_service() -> ProductService:
    """Factory local para construir ProductService con sus dependencias (DI manual)."""
    return ProductService(repo=DjangoProductRepository())


class ProductRegisterView(APIView):
    """POST /api/products/
    Registra un nuevo producto en el catálogo. Solo usuarios autenticados.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RegisterProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            product = service.register_product(
                name=str(data["name"]),
                description=str(data.get("description", "")),
                price=data["price"],
                stock=int(data["stock"]),
            )
        except InvalidProductData as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        output = ProductOutputSerializer(product)
        return Response(output.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    """GET /api/products/<product_id>/
    Obtiene el detalle de un producto por su UUID.
    """

    def get(self, request, product_id):
        service = _build_service()
        product = service._repo.get_by_id(product_id)

        if product is None:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        output = ProductOutputSerializer(product)
        return Response(output.data, status=status.HTTP_200_OK)