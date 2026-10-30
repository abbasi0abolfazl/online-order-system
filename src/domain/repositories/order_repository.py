from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.order import Order
from ..value_objects.address import Address


class OrderRepository(ABC):
    """Repository Pattern"""
    
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def find_by_customer_id(self, customer_id: str) -> List[Order]:
        pass
    
    @abstractmethod
    def update(self, order: Order) -> Order:
        pass
    
    @abstractmethod
    def delete(self, order_id: str) -> bool:
        pass
    
    @abstractmethod
    def find_by_status(self, status: str) -> List[Order]:
        pass