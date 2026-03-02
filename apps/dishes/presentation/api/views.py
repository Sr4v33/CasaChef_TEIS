from typing import cast, Dict, Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.dishes.application.services.product_service import ProductService
from apps.dishes.domain.exceptions import InvalidProductData
from apps.dishes.infrastructure.repositories.django_product_repository import DjangoProductRepository
from apps.dishes.presentation.api.serializers import (
    RegisterProductSerializer,
    ProductOutputSerializer,
)


def _build_service() -> ProductService:
    return ProductService(repo=DjangoProductRepository())


class ProductRegisterView(APIView):
    """POST /api/products/ — Registra un producto en el catálogo."""

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
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ProductOutputSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    """GET /api/products/<product_id>/ — Obtiene un producto por UUID."""

    def get(self, request, product_id):
        service = _build_service()
        product = service._repo.get_by_id(product_id)

        if product is None:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response(ProductOutputSerializer(product).data, status=status.HTTP_200_OK)


class ProductByNameView(APIView):
    """GET /api/products/by-name/?name=<nombre> - Obtiene un producto por su nombre."""

    def get(self, request):
        name = request.query_params.get("name", "").strip()
        if not name:
            return Response(
                {"error": "El parámetro 'name' es obligatorio"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = _build_service()
        product = service._repo.get_by_name(name)

        if product is None:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        return Response(ProductOutputSerializer(product).data, status=status.HTTP_200_OK)