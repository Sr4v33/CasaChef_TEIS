from apps.payments.domain.entities.payment import PaymentEntity, PaymentMethod, PaymentStatus
from apps.payments.infrastructure.models.payment_model import PaymentModel


class PaymentMapper:
    @staticmethod
    def to_domain(model: PaymentModel) -> PaymentEntity:
        return PaymentEntity(
            payment_id=model.id,
            method=PaymentMethod(model.method),
            status=PaymentStatus(model.status),
            transaction_reference=model.transaction_reference,
        )

    @staticmethod
    def to_model(entity: PaymentEntity) -> dict:
        return {
            "id": entity.payment_id,
            "method": entity.method.value,
            "status": entity.status.value,
            "transaction_reference": entity.transaction_reference,
        }
