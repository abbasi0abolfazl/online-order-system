import sys
import os

# اضافه کردن مسیر پروژه به sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from infrastructure.persistence.sqlite_order_repository import SQLiteOrderRepository
from infrastructure.event_publishers.order_event_publisher import LoggingEventPublisher
from application.command_handlers.order_command_handler import OrderCommandHandler
from application.query_handlers.order_query_handler import OrderQueryHandler


class DependencyContainer:
    """Singleton Pattern for dependency management"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_dependencies()
        return cls._instance
    
    def _init_dependencies(self):
        # Initialize repositories
        self.order_repository = SQLiteOrderRepository("orders.db")
        
        # Initialize event publishers
        self.event_publisher = LoggingEventPublisher()
        
        # Initialize command and query handlers
        self.order_command_handler = OrderCommandHandler(
            repository=self.order_repository,
            event_publisher=self.event_publisher
        )
        self.order_query_handler = OrderQueryHandler(
            repository=self.order_repository
        )
    
    @classmethod
    def get_instance(cls):
        """Factory Method for getting singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
class DependencyContainer:
    """Singleton Pattern for dependency management"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_dependencies()
        return cls._instance
    
    def _init_dependencies(self):
        # Initialize repositories
        self.order_repository = SQLiteOrderRepository("orders.db")
        
        # Initialize event publishers
        self.event_publisher = LoggingEventPublisher()
        
        # Initialize command and query handlers
        self.order_command_handler = OrderCommandHandler(
            repository=self.order_repository,
            event_publisher=self.event_publisher
        )
        self.order_query_handler = OrderQueryHandler(
            repository=self.order_repository
        )
    
    @classmethod
    def get_instance(cls):
        """Factory Method for getting singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance