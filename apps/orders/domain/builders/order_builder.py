# apps/orders/domain/entities.py
from ..entities.order import OrderEntity
from ..entities.order_item import OrderItemEntity
from ..ports.production_repository_port import ProductionRepository


class OrderBuilder:
    def __init__(self, production_repo: ProductionRepository):
        self._production_repo = production_repo
        self._user_id = 0
        self._items = []
        self._address = ''
        self._date = ''

    def for_user(self, user_id: int):
        self._user_id = user_id
        return self

    def with_items(self, items: list):
        for it in items:
            self._items.append(
                OrderItemEntity(
                    dish_id=it["dish_id"],
                    quantity=it.get("quantity", it.get("qty")), # Robusto a ambos nombres
                    unit_price=it.get("unit_price", it.get("price")),
                )
            )
        return self

    def to_address(self, address: str):
        self._address = address
        return self

    def for_date(self, date: str):
        self._date = date
        return self

    def build(self) -> OrderEntity:
        self._validate_required_data()
        self._validate_and_reserve_production()

        return OrderEntity(
            user_id=self._user_id,
            address=self._address,
            date=self._date,
            items=self._items,
        )

    def _validate_required_data(self):
        if not self._user_id:
            raise ValueError("User requerido")
        if not self._items:
            raise ValueError("Items requeridos")
        if not self._date:
            raise ValueError("Fecha requerida")

    def _validate_and_reserve_production(self):
        for item in self._items:
            self._production_repo.check_and_reserve(
                dish_id=item.dish_id,
                date=self._date,
                quantity=item.quantity,
            )
