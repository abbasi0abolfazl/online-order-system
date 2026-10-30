from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.order_router import router as order_router
import uvicorn
from contextlib import asynccontextmanager
import sqlite3


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    print("Starting Order Service...")
    
    # Initialize database
    conn = sqlite3.connect("orders.db")
    conn.close()
    
    yield
    
    # Shutdown
    print("Shutting down Order Service...")


# Create FastAPI application
app = FastAPI(
    title="Order Management Service",
    description="Microservice for managing customer orders",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(order_router)

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "order-service",
        "timestamp": "2024-01-15T10:30:00Z"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )