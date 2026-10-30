from typing import Dict
from ..commands.create_order_command import CreateOrderCommand
from ..commands.update_order_command import UpdateOrderStatusCommand
from ...domain.entities.order import Order, OrderItem, OrderStatus
from ...domain.repositories.order_repository import OrderRepository
from ...infrastructure.event_publishers.order_event_publisher import OrderEventPublisher
import uuid


class OrderCommandHandler:
    """Command Handler with Strategy Pattern"""
    
    def __init__(self, 
                 repository: OrderRepository,
                 event_publisher: OrderEventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher
    
    def handle_create_order(self, command: CreateOrderCommand) -> Dict:
        # Factory Method Pattern
        order_items = [
            OrderItem(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price
            ) for item in command.items
        ]
        
        order = Order(
            order_id=str(uuid.uuid4()),
            customer_id=command.customer_id,
            items=order_items
        )
        
        saved_order = self.repository.save(order)
        
        # Publish domain event (Event-Driven optional)
        self.event_publisher.publish_order_created(saved_order)
        
        return {
            "order_id": saved_order.order_id,
            "status": saved_order.status.value,
            "total_amount": saved_order.total_amount,
            "created_at": saved_order.created_at.isoformat()
        }
    
    def handle_update_order_status(self, command: UpdateOrderStatusCommand) -> Dict:
        order = self.repository.find_by_id(command.order_id)
        
        if not order:
            raise ValueError(f"Order {command.order_id} not found")
        
        order.update_status(command.new_status)
        updated_order = self.repository.update(order)
        
        # Publish event
        self.event_publisher.publish_order_status_changed(updated_order)
        
        return {
            "order_id": updated_order.order_id,
            "new_status": updated_order.status.value,
            "updated_at": updated_order.updated_at.isoformat()
        }