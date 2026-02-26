from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any


class DiscountPolicyPort(ABC):
    """Contrato de una política de descuentos (Strategy).
    Para mantener SRP, la regla de descuento vive en una política
    (extensible) y el Product solo la *usa*.
    """

    # Revisar este metodo
    @abstractmethod
    def get_discount_amount(self, *, product: Any, customer: Any | None = None) -> Decimal:
        """Retorna el valor de descuento (en dinero) para el producto."""
        raise NotImplementedError
