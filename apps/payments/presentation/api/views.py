from typing import cast, Dict, Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.payments.application.services.payment_service import PaymentService
from apps.payments.domain.entities.payment import PaymentMethod
from apps.payments.domain.exceptions import (
    InvalidPaymentData,
    InvalidPaymentTransition,
    PaymentProcessingError,
)
from apps.payments.infrastructure.repositories.django_payment_repository import DjangoPaymentRepository
from apps.payments.presentation.api.serializers import (
    PayOrderSerializer,
    PaymentOutputSerializer,
)


def _build_service() -> PaymentService:
    """Factory local para inyectar dependencias en PaymentService."""
    return PaymentService(repo=DjangoPaymentRepository())


class PayOrderView(APIView):
    """POST /api/payments/
    Procesa el pago de una orden existente.
    El procesador de pago se selecciona por Factory (env var PAYMENT_PROVIDER).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PayOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            payment = service.pay_order(
                order_id=int(data["order_id"]),
                amount=data["amount"],
                method=PaymentMethod(data["method"]),
            )
        except (InvalidPaymentData, InvalidPaymentTransition) as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except PaymentProcessingError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        output = PaymentOutputSerializer(payment)
        return Response(output.data, status=status.HTTP_201_CREATED)


class PaymentDetailView(APIView):
    """GET /api/payments/<payment_id>/
    Obtiene el detalle de un pago por su UUID.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        service = _build_service()
        payment = service._repo.get_by_id(payment_id)

        if payment is None:
            return Response({"error": "Pago no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        output = PaymentOutputSerializer(payment)
        return Response(output.data, status=status.HTTP_200_OK)