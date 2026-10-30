class DependencyContainer:
    """Simple dependency container"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_dependencies()
        return cls._instance
    
    def _init_dependencies(self):
        self.order_repository = None
        self.event_publisher = None
        self.order_command_handler = None
        self.order_query_handler = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
