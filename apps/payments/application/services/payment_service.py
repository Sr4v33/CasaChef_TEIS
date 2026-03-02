from decimal import Decimal
from typing import Any, Mapping, Optional
from uuid import UUID

from apps.payments.domain.entities.payment import PaymentEntity, PaymentMethod
from apps.payments.domain.ports.payment_repository_port import PaymentRepositoryPort
from apps.payments.infrastructure.factories.payment_factory import PaymentFactory


class PaymentService:
    """Service Layer para casos de uso de pago.

    Expone métodos públicos para todos los casos de uso. Ninguna vista debe
    acceder a _repo directamente: toda consulta pasa por este servicio.
    """

    def __init__(self, repo: PaymentRepositoryPort) -> None:
        self._repo = repo

    def pay_order(
        self,
        *,
        order_id: int,
        amount: Decimal,
        method: PaymentMethod,
        metadata: Mapping[str, Any] | None = None,
    ) -> PaymentEntity:
        """Procesa el pago de una orden y lo persiste."""
        payment = PaymentEntity(method=method)

        processor = PaymentFactory.create()
        payment.process_payment(amount=amount, processor=processor, metadata=metadata)

        # Confirmación inmediata (lógica asíncrona queda pendiente según proveedor)
        payment.confirm_payment()

        payment = self._repo.save(payment)
        return payment

    def get_payment(self, payment_id: UUID) -> Optional[PaymentEntity]:
        """Retorna un pago por su UUID o None si no existe.

        Las vistas deben usar este método en lugar de acceder a _repo directamente.
        """
        return self._repo.get_by_id(payment_id)