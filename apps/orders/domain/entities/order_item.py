from dataclasses import dataclass

@dataclass
class OrderItemEntity:
    dish_id: int
    quantity: int
    unit_price: float