from abc import ABC, abstractmethod


class ProductionRepository(ABC):

    @abstractmethod
    def check_and_reserve(self, dish_id: int, date: str, quantity: int) -> None:
        pass

    @abstractmethod
    def check_stock(self, dish_id: int, quantity: int) -> bool:
        """Verifica sin reservar si hay stock disponible. Retorna True si hay suficiente."""
        pass