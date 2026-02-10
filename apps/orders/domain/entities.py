# apps/orders/domain/entities.py

from dataclasses import dataclass
from typing import List


@dataclass
class OrderItemEntity:
    dish_id: int
    quantity: int
    unit_price: float


@dataclass
class OrderEntity:
    user_id: int
    address: str
    date: str
    items: List[OrderItemEntity]
    status: str = "CONFIRMED"

    def total_amount(self) -> float:
        return sum(i.quantity * i.unit_price for i in self.items)
