# Django autodiscovery shim for clean-architecture models
from apps.orders.infraestructure.models.order_item_model import OrderItem  # noqa: F401 
from apps.orders.infraestructure.models.order_model import Order  # noqa: F401

# Import no usado, pero intencional