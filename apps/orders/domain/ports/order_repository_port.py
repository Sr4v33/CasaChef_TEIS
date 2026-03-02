from abc import ABC, abstractmethod
from typing import Optional

from apps.orders.domain.entities.order import OrderEntity


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: OrderEntity) -> int:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[OrderEntity]:
        pass

    @abstractmethod
    def update(self, order: OrderEntity) -> None:
        pass