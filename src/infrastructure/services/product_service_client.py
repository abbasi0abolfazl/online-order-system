import requests
from abc import ABC, abstractmethod


class ProductServiceClient(ABC):
    """Adapter Pattern for external service communication"""
    
    @abstractmethod
    def get_product_details(self, product_id: str) -> dict:
        pass
    
    @abstractmethod
    def validate_product_availability(self, product_id: str, quantity: int) -> bool:
        pass


class HTTPProductServiceClient(ProductServiceClient):
    """Adapter implementation using HTTP"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def get_product_details(self, product_id: str) -> dict:
        try:
            response = requests.get(f"{self.base_url}/products/{product_id}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch product details: {e}")
    
    def validate_product_availability(self, product_id: str, quantity: int) -> bool:
        try:
            response = requests.post(
                f"{self.base_url}/products/{product_id}/check-availability",
                json={"required_quantity": quantity},
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("available", False)
        except requests.RequestException:
            return False