from typing import cast, Dict, Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.orders.application.services.order_service import OrderService
from apps.orders.domain.exceptions import (
    OrderDomainError,
    OrderNotFoundError,
    InvalidOrderTransition,
    InsufficientProductionStock,
)
from apps.orders.infrastructure.repositories.django_order_repository import DjangoOrderRepository
from apps.orders.infrastructure.repositories.django_production_repository import DjangoProductionRepository
from apps.orders.infrastructure.factories.notifier_factory import NotifierFactory
from apps.orders.presentation.api.serializers import (
    CreateOrderSerializer,
    OrderOutputSerializer,
)


def _build_service() -> OrderService:
    return OrderService(
        order_repo=DjangoOrderRepository(),
        production_repo=DjangoProductionRepository(),
        notifier=NotifierFactory.create(),
    )


class OrderCreateView(APIView):
    """POST /api/orders/ — Crea una orden y reserva cupos de producción."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        data["date"] = str(data["date"])
        data["items"] = [
            {
                "dish_id":    item["dish_id"],
                "quantity":   item["quantity"],
                "unit_price": float(item["unit_price"]),
            }
            for item in data["items"]
        ]

        service = _build_service()
        try:
            order_id = service.create_order(user=request.user, data=data)
        except InsufficientProductionStock as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except OrderDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response({"order_id": order_id}, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    """GET /api/orders/<order_id>/ — Detalle de una orden (solo propietario)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id: int):
        service = _build_service()
        # Uso del método público del servicio, sin acceder a _order_repo
        order = service.get_order(order_id)

        if order is None:
            return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        if order.user_id != request.user.id:
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)

        return Response(OrderOutputSerializer(order).data, status=status.HTTP_200_OK)


class OrderConfirmView(APIView):
    """PATCH /api/orders/<order_id>/confirm/ — Confirma una orden PENDING."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id: int):
        service = _build_service()
        try:
            service.confirm_order(order_id)
        except OrderNotFoundError:
            return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidOrderTransition as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except OrderDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": f"Orden {order_id} confirmada"}, status=status.HTTP_200_OK)


class OrderCancelView(APIView):
    """PATCH /api/orders/<order_id>/cancel/ — Cancela una orden PENDING o CONFIRMED."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id: int):
        service = _build_service()
        try:
            service.cancel_order(order_id)
        except OrderNotFoundError:
            return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidOrderTransition as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except OrderDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": f"Orden {order_id} cancelada"}, status=status.HTTP_200_OK)


class OrderValidateStockView(APIView):
    """GET /api/orders/<order_id>/validate-stock/ — Valida stock de producción para todos los ítems."""

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id: int):
        service = _build_service()
        try:
            service.validate_stock(order_id)
        except OrderNotFoundError:
            return Response({"error": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except OrderDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(
            {"detail": "Stock de producción disponible para todos los ítems"},
            status=status.HTTP_200_OK,
        )