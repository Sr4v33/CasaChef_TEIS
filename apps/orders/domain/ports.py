# apps/orders/domain/ports.py
from abc import ABC, abstractmethod
from typing import List
from .entities import OrderEntity


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: OrderEntity) -> int:
        pass


class ProductionRepository(ABC):

    @abstractmethod
    def check_and_reserve(self, dish_id: int, date: str, quantity: int):
        pass
