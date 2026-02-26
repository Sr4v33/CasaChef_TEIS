from decimal import Decimal
from typing import Any, Mapping

from apps.payments.domain.entities.payment import PaymentEntity, PaymentMethod
from apps.payments.domain.ports.payment_repository_port import PaymentRepositoryPort
from apps.payments.infrastructure.factories.payment_factory import PaymentFactory


class PaymentService:
    """Service Layer para casos de uso de pago.

    Separa la orquestación del framework y de la vista (testabilidad y portabilidad).
    """

    def __init__(self, repo: PaymentRepositoryPort):
        self._repo = repo

    def pay_order(
        self,
        *,
        order_id: int,
        amount: Decimal,
        method: PaymentMethod,
        metadata: Mapping[str, Any] | None = None,
    ) -> PaymentEntity:
        payment = PaymentEntity(method=method)

        processor = PaymentFactory.create()
        payment.process_payment(amount=amount, processor=processor, metadata=metadata)

        # Aquí hace falta lógica de confirmación asincrónica dependiendo del proveedor.
        payment.confirm_payment()

        # Persistencia (si aplica)
        payment = self._repo.save(payment)

        # Aquí iría el vínculo order_id del modelo (cuando exista repositorio/mapper completo).
        # Ej: self._repo.attach_to_order(payment_id=payment.payment_id, order_id=order_id)

        return payment
