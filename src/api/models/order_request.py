from pydantic import BaseModel, validator
from typing import List


class OrderItemRequest(BaseModel):
    product_id: str
    quantity: int
    
    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        return v


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItemRequest]
    shipping_address: dict


class UpdateOrderStatusRequest(BaseModel):
    new_status: str