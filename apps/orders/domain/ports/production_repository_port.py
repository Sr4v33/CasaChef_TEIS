from abc import ABC, abstractmethod


class ProductionRepository(ABC):

    @abstractmethod
    def check_and_reserve(self, dish_id: int, date: str, quantity: int) -> None:
        pass

    @abstractmethod
    def check_stock(self, dish_id: int, date: str, quantity: int) -> bool:
        """Verifica cupos en la fecha indicada (sin reservar).

        Para pedidos ya creados, la reserva previa se suma a los cupos restantes.
        """
        pass