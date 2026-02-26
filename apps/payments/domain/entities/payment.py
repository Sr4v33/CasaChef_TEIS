from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Any, Mapping, Optional

from ..exceptions import InvalidPaymentData, InvalidPaymentTransition, PaymentProcessingError
from ..ports.payment_processor_port import PaymentProcessorPort


class PaymentMethod(str, Enum):
    CARD = "CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    CASH = "CASH"
    # Si el negocio define otros métodos, agregarlos aquí (OCP).


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"


@dataclass(slots=True)
class Payment:
    """Entidad de dominio Payment.

    Se sugiere que entidades como Producto/Orden tengan métodos de negocio
    como `procesar_pago()` (no solo datos).
    """

    method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_reference: Optional[str] = None

    payment_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self) -> None:
        if not isinstance(self.method, PaymentMethod):
            # Permitir que llegue string desde API y lo normalizamos
            try:
                self.method = PaymentMethod(str(self.method))
            except Exception as exc:  # pragma: no cover
                raise InvalidPaymentData("Método de pago inválido") from exc

        if not isinstance(self.status, PaymentStatus):
            try:
                self.status = PaymentStatus(str(self.status))
            except Exception as exc:  # pragma: no cover
                raise InvalidPaymentData("Estado de pago inválido") from exc

        if self.transaction_reference is not None:
            self.transaction_reference = self.transaction_reference.strip() or None

    # -----------------------------
    # Métodos de negocio
    # -----------------------------

    def process_payment(
        self,
        *,
        amount: Decimal,
        processor: PaymentProcessorPort,
        metadata: Mapping[str, Any] | None = None,
    ) -> str:
        """Intenta procesar el pago usando un procesador (abstracción).

        - DIP: PaymentEntity depende de PaymentProcessorPort (interfaz), no de un banco/paypal concreto.
        - Factory Method (en infraestructura): permite elegir el procesador por configuración de entorno, sin tocar la vista.
        """
        amount = self._validate_amount(amount)

        if self.status != PaymentStatus.PENDING:
            raise InvalidPaymentTransition("Solo se puede procesar un pago en estado PENDING")

        try:
            tx_ref = processor.process(amount=amount, metadata=metadata)
        except Exception as exc:
            # No filtramos la excepción de infraestructura al dominio
            self.mark_failed()
            raise PaymentProcessingError("No fue posible procesar el pago") from exc

        self.transaction_reference = tx_ref
        return tx_ref

    def confirm_payment(self) -> None:
        if self.status == PaymentStatus.CONFIRMED:
            return
        if self.status != PaymentStatus.PENDING:
            raise InvalidPaymentTransition("Solo se puede confirmar un pago en estado PENDING")
        if not self.transaction_reference:
            raise InvalidPaymentData("No se puede confirmar sin transaction_reference")
        self.status = PaymentStatus.CONFIRMED

    def mark_failed(self) -> None:

        self.status = PaymentStatus.FAILED
        # No levantamos excepción: fallar es un estado final válido

    # -----------------------------
    # Helpers
    # -----------------------------

    def _validate_amount(self, amount: Any) -> Decimal:
        try:
            d = amount if isinstance(amount, Decimal) else Decimal(str(amount))
        except Exception as exc:  # pragma: no cover
            raise InvalidPaymentData("La cantidad debe ser numérica") from exc
        if d <= 0:
            raise InvalidPaymentData("La cantidad debe ser mayor a 0")
        return d


# Alias para compatibilidad con otros módulos
PaymentEntity = Payment
