from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from enum import Enum

router = APIRouter(prefix="/orders", tags=["orders"])

# Enums and Models
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price

class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItem]
    shipping_address: dict

class UpdateOrderRequest(BaseModel):
    status: Optional[OrderStatus] = None
    items: Optional[List[OrderItem]] = None

# In-memory database
orders_db = {}

@router.get("/")
async def get_all_orders(status: Optional[str] = None, customer_id: Optional[str] = None):
    """Get all orders with optional filtering"""
    filtered_orders = list(orders_db.values())
    
    if status:
        filtered_orders = [o for o in filtered_orders if o["status"] == status]
    
    if customer_id:
        filtered_orders = [o for o in filtered_orders if o["customer_id"] == customer_id]
    
    return {
        "count": len(filtered_orders),
        "orders": filtered_orders
    }

@router.get("/{order_id}")
async def get_order(order_id: str):
    """Get order by ID"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

@router.post("/", status_code=201)
async def create_order(request: CreateOrderRequest):
    """Create a new order"""
    order_id = str(uuid.uuid4())
    
    # Calculate total amount
    total_amount = sum(item.total_price for item in request.items)
    
    order = {
        "order_id": order_id,
        "customer_id": request.customer_id,
        "items": [item.dict() for item in request.items],
        "shipping_address": request.shipping_address,
        "status": OrderStatus.PENDING.value,
        "total_amount": total_amount,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    orders_db[order_id] = order
    
    return {
        "message": "Order created successfully",
        "order_id": order_id,
        "status": order["status"],
        "total_amount": total_amount
    }

@router.put("/{order_id}")
async def update_order(order_id: str, request: UpdateOrderRequest):
    """Update an existing order"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = orders_db[order_id]
    
    # Update status if provided
    if request.status:
        order["status"] = request.status.value
    
    # Update items if provided
    if request.items:
        order["items"] = [item.dict() for item in request.items]
        # Recalculate total
        order["total_amount"] = sum(item.total_price for item in request.items)
    
    order["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": "Order updated successfully",
        "order": order
    }

@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, status: OrderStatus):
    """Update only order status"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    orders_db[order_id]["status"] = status.value
    orders_db[order_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": "Order status updated",
        "order_id": order_id,
        "new_status": status.value
    }

@router.delete("/{order_id}")
async def delete_order(order_id: str):
    """Delete an order"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    deleted_order = orders_db.pop(order_id)
    
    return {
        "message": "Order deleted successfully",
        "order_id": order_id,
        "deleted_order": deleted_order
    }

@router.get("/customer/{customer_id}")
async def get_customer_orders(customer_id: str):
    """Get all orders for a specific customer"""
    customer_orders = [o for o in orders_db.values() if o["customer_id"] == customer_id]
    
    return {
        "customer_id": customer_id,
        "count": len(customer_orders),
        "orders": customer_orders
    }


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import order_router
import uvicorn
import sqlite3
from datetime import datetime

app = FastAPI(
    title="Order Management Service",
    description="Microservice for managing customer orders",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
def init_db():
    conn = sqlite3.connect("orders.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL,
            items TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Include routers - THIS IS THE CRITICAL PART
app.include_router(order_router.router)

@app.get("/")
async def root():
    return {"message": "Order Service is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "order-service",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Initialize database on startup
    init_db()
    print("Database initialized")
    
    uvicorn.run(
        app,  # Change this from "api.main:app" to just "app"
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )