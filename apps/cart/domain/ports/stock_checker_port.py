from abc import ABC, abstractmethod
from uuid import UUID


class StockCheckerPort(ABC):
    """Contrato para verificar disponibilidad de stock (DIP).

    Cart.validate_availability() depende de esta abstracción,
    no de modelos de infraestructura concretos.
    """

    @abstractmethod
    def check(self, product_id: UUID, quantity: int) -> None:
        """Verifica que el producto tenga stock suficiente.

        Debe lanzar una excepción de dominio si el stock es insuficiente,
        para que el error pueda ser capturado limpiamente en el service layer.
        """
        raise NotImplementedError