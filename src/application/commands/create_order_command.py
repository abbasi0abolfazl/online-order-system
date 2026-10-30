from dataclasses import dataclass
from typing import List
from ..dtos.order_item_dto import OrderItemDTO


@dataclass
class CreateOrderCommand:
    """Command for CQRS"""
    customer_id: str
    items: List[OrderItemDTO]
    shipping_address: dict