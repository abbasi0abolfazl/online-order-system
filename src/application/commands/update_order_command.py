from dataclasses import dataclass
from ...domain.entities.order import OrderStatus


@dataclass
class UpdateOrderStatusCommand:
    order_id: str
    new_status: OrderStatus