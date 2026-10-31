from dataclasses import dataclass


@dataclass
class OrderItemDTO:
    """Data Transfer Object for Order Items"""
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
