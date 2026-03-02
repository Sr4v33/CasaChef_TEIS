from typing import cast, Dict, Any
from decimal import Decimal
from uuid import UUID

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.cart.application.services.cart_service import CartService
from apps.cart.domain.exceptions import (
    CartDomainError,
    CartIsEmptyError,
    ProductNotInCartError,
    InvalidCartItemData,
)
from apps.cart.infrastructure.repositories.django_cart_repository import DjangoCartRepository
from apps.cart.infrastructure.repositories.product_stock_checker import ProductStockChecker
from apps.cart.presentation.api.serializers import (
    AddProductSerializer,
    RemoveProductSerializer,
    CartOutputSerializer,
)


def _build_service() -> CartService:
    return CartService(
        cart_repo=DjangoCartRepository(),
        stock_checker=ProductStockChecker(),
    )


class CartDetailView(APIView):
    """GET /api/cart/ — Carrito activo del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = _build_service()
        cart = service.get_cart(customer_id=request.user.id)
        return Response(CartOutputSerializer(cart).data, status=status.HTTP_200_OK)


class CartAddProductView(APIView):
    """POST /api/cart/items/ — Añade un producto al carrito."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            cart = service.add_product(
                customer_id=request.user.id,
                product_id=UUID(str(data["product_id"])),
                quantity=int(data["quantity"]),
                unit_price=Decimal(str(data["unit_price"])),
            )
        except InvalidCartItemData as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except CartDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(CartOutputSerializer(cart).data, status=status.HTTP_200_OK)


class CartRemoveProductView(APIView):
    """DELETE /api/cart/items/ — Elimina un producto del carrito."""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = RemoveProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            cart = service.remove_product(
                customer_id=request.user.id,
                product_id=UUID(str(data["product_id"])),
            )
        except (ProductNotInCartError, CartIsEmptyError) as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(CartOutputSerializer(cart).data, status=status.HTTP_200_OK)


class CartTotalView(APIView):
    """GET /api/cart/total/ — Total del carrito."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = _build_service()
        try:
            total = service.calculate_total(customer_id=request.user.id)
        except CartIsEmptyError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"total": str(total)}, status=status.HTTP_200_OK)


class CartValidateView(APIView):
    """POST /api/cart/validate/ — Valida stock para todos los ítems."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        service = _build_service()
        try:
            service.validate_availability(customer_id=request.user.id)
        except CartIsEmptyError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except CartDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(
            {"detail": "Stock disponible para todos los productos"},
            status=status.HTTP_200_OK,
        )


class CartClearView(APIView):
    """DELETE /api/cart/ - Vacía el carrito del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        service = _build_service()
        # clear_cart no lanza excepción si el carrito no existe — es idempotente
        service.clear_cart(customer_id=request.user.id)

        # 204: operación exitosa, no hay cuerpo que devolver
        return Response(status=status.HTTP_204_NO_CONTENT)