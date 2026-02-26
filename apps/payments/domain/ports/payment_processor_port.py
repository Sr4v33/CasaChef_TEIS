from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Mapping


class PaymentProcessorPort(ABC):
    """Abstracción para procesar pagos (DIP).

    Depender de abstracciones y no de implementaciones concretas.
    """

    @abstractmethod
    def process(self, *, amount: Decimal, metadata: Mapping[str, Any] | None = None) -> str:
        """Procesa un pago y retorna un transaction_reference."""
        raise NotImplementedError
