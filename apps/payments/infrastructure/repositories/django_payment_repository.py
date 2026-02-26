from decimal import Decimal
from typing import Optional
from uuid import UUID

from apps.payments.domain.entities.payment import PaymentEntity
from apps.payments.domain.ports.payment_repository_port import PaymentRepositoryPort
from apps.payments.infrastructure.mappers.payment_mapper import PaymentMapper
from apps.payments.infrastructure.models.payment_model import PaymentModel


class DjangoPaymentRepository(PaymentRepositoryPort):
    def save(self, payment: PaymentEntity) -> PaymentEntity:
        # amount/currency/order_id deben ser provistos por el caso de uso.
        # Aquí dejamos defaults seguros.
        defaults = PaymentMapper.to_model(payment)
        defaults.setdefault("amount", Decimal("0.01"))
        defaults.setdefault("currency", "COP")
        PaymentModel.objects.update_or_create(id=payment.payment_id, defaults=defaults)
        return payment

    def get_by_id(self, payment_id: UUID) -> Optional[PaymentEntity]:
        try:
            m = PaymentModel.objects.get(id=payment_id)
        except PaymentModel.DoesNotExist:
            return None
        return PaymentMapper.to_domain(m)
