from decimal import Decimal
from typing import Any, Mapping
import uuid

from apps.payments.domain.ports.payment_processor_port import PaymentProcessorPort


class MockPaymentProcessor(PaymentProcessorPort):
    """Procesador falso para DEV/tests."""

    def process(self, *, amount: Decimal, metadata: Mapping[str, Any] | None = None) -> str:
        # Simula un transaction_reference (sin I/O real)
        return f"MOCK-{uuid.uuid4()}"
