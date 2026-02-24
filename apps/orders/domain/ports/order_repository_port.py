from abc import ABC, abstractmethod
from apps.orders.domain.entities.order import OrderEntity

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: OrderEntity) -> int:
        pass


