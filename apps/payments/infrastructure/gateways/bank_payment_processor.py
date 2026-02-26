from decimal import Decimal
from typing import Any, Mapping
import uuid

from apps.payments.domain.ports.payment_processor_port import PaymentProcessorPort


class BankPaymentProcessor(PaymentProcessorPort):
    """Placeholder de integración con un banco real.

    # Aquí iría el SDK/HTTP client del proveedor y manejo de errores.
    """

    def process(self, *, amount: Decimal, metadata: Mapping[str, Any] | None = None) -> str:
        # Simulación: en la integración real se retornaría el reference del banco.
        return f"BANK-{uuid.uuid4()}"
