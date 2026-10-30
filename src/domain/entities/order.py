from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    """Value Object"""
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float = field(init=False)
    
    def __post_init__(self):
        self.total_price = self.quantity * self.unit_price
        self._validate()
    
    def _validate(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price <= 0:
            raise ValueError("Unit price must be positive")


@dataclass
class Order:
    """Aggregate Root"""
    order_id: str
    customer_id: str
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    total_amount: float = field(init=False)
    
    def __post_init__(self):
        self.total_amount = sum(item.total_price for item in self.items)
        self._validate()
    
    def _validate(self):
        if not self.items:
            raise ValueError("Order must have at least one item")
    
    def update_status(self, new_status: OrderStatus):
        """Domain Event could be triggered here"""
        self.status = new_status
        self.updated_at = datetime.now()
    
    def calculate_total(self) -> float:
        return sum(item.total_price for item in self.items)
    
    def add_item(self, item: OrderItem):
        self.items.append(item)
        self.total_amount = self.calculate_total()
        self.updated_at = datetime.now()
    
    def remove_item(self, product_id: str):
        self.items = [item for item in self.items if item.product_id != product_id]
        self.total_amount = self.calculate_total()
        self.updated_at = datetime.now()