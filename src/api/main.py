from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import order_router
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

# Include routers
try:
    app.include_router(order_router.router)
except Exception as e:
    print(f"Warning: Could not load order router: {e}")

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
        "api.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )