from abc import ABC, abstractmethod

class ProductionRepository(ABC):
    @abstractmethod
    def check_and_reserve(self, dish_id: int, date: str, quantity: int):
        pass
