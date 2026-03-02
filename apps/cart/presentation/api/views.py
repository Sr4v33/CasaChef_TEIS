from typing import cast, Dict, Any
from decimal import Decimal
from uuid import UUID

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.cart.application.services.cart_service import CartService
from apps.cart.domain.exceptions import CartDomainError, CartIsEmptyError, ProductNotInCartError
from apps.cart.infrastructure.repositories.django_cart_repository import DjangoCartRepository
from apps.cart.infrastructure.repositories.product_stock_checker import ProductStockChecker
from apps.cart.presentation.api.serializers import (
    AddProductSerializer,
    RemoveProductSerializer,
    CartOutputSerializer,
)


def _build_service() -> CartService:
    """Factory local para construir el CartService con sus dependencias.

    En un proyecto más grande esto lo haría un contenedor DI (ej. dependency-injector).
    """
    return CartService(
        cart_repo=DjangoCartRepository(),
        stock_checker=ProductStockChecker(),
    )


class CartDetailView(APIView):
    """GET /cart/ — Obtiene el carrito activo del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = _build_service()
        cart = service.get_cart(customer_id=request.user.id)
        serializer = CartOutputSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartAddProductView(APIView):
    """POST /cart/items/ — Añade un producto al carrito."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # cast necesario: Pylance infiere validated_data como `empty | dict`
        # hasta que is_valid() retorna True, pero no lo estrecha automáticamente.
        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()
        try:
            cart = service.add_product(
                customer_id=request.user.id,
                product_id=UUID(str(data["product_id"])),
                quantity=int(data["quantity"]),
                unit_price=Decimal(str(data["unit_price"])),
            )
        except CartDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)

        output = CartOutputSerializer(cart)
        return Response(output.data, status=status.HTTP_200_OK)


class CartRemoveProductView(APIView):
    """DELETE /cart/items/ — Elimina un producto del carrito."""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = RemoveProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # cast necesario por el mismo motivo que en CartAddProductView
        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()
        try:
            cart = service.remove_product(
                customer_id=request.user.id,
                product_id=UUID(str(data["product_id"])),
            )
        except ProductNotInCartError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except CartIsEmptyError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        output = CartOutputSerializer(cart)
        return Response(output.data, status=status.HTTP_200_OK)


class CartTotalView(APIView):
    """GET /cart/total/ — Retorna el total del carrito."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = _build_service()
        try:
            total = service.calculate_total(customer_id=request.user.id)
        except CartIsEmptyError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"total": str(total)}, status=status.HTTP_200_OK)


class CartValidateView(APIView):
    """POST /cart/validate/ — Valida disponibilidad de stock para el carrito."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        service = _build_service()
        try:
            service.validate_availability(customer_id=request.user.id)
        except (CartDomainError, CartIsEmptyError) as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(
            {"detail": "Stock disponible para todos los productos"},
            status=status.HTTP_200_OK,
        )