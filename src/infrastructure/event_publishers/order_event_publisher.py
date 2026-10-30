from abc import ABC, abstractmethod
from ...domain.entities.order import Order
import json


class OrderEventPublisher(ABC):
    """Observer Pattern for event publishing"""
    
    @abstractmethod
    def publish_order_created(self, order: Order):
        pass
    
    @abstractmethod
    def publish_order_status_changed(self, order: Order):
        pass


class LoggingEventPublisher(OrderEventPublisher):
    """Concrete implementation that logs events"""
    
    def publish_order_created(self, order: Order):
        event = {
            "event_type": "OrderCreated",
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "total_amount": order.total_amount,
            "timestamp": order.created_at.isoformat()
        }
        print(f"[Event Published]: {json.dumps(event, indent=2)}")
    
    def publish_order_status_changed(self, order: Order):
        event = {
            "event_type": "OrderStatusChanged",
            "order_id": order.order_id,
            "new_status": order.status.value,
            "timestamp": order.updated_at.isoformat()
        }
        print(f"[Event Published]: {json.dumps(event, indent=2)}")