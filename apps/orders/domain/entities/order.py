from dataclasses import dataclass
from apps.orders.domain.entities.order_item import OrderItemEntity
from typing import List

@dataclass
class OrderEntity:
    user_id: int
    address: str
    date: str
    items: List[OrderItemEntity]
    status: str = "CONFIRMED"

    def total_amount(self) -> float:
        return sum(i.quantity * i.unit_price for i in self.items)
