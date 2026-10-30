from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

app = FastAPI(
    title="User Service",
    description="Microservice for managing users",
    version="1.0.0"
)

# Models
class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None

# In-memory database
users_db = {}

@app.get("/")
async def root():
    return {
        "message": "User Service is running",
        "endpoints": {
            "GET /users": "Get all users",
            "POST /users": "Create user",
            "GET /users/{user_id}": "Get user by ID",
            "PUT /users/{user_id}": "Update user",
            "DELETE /users/{user_id}": "Delete user"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "user-service",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/users")
async def get_users():
    """Get all users"""
    return {
        "count": len(users_db),
        "users": list(users_db.values())
    }

@app.post("/users", status_code=201)
async def create_user(user: UserCreate):
    """Create a new user"""
    user_id = str(uuid.uuid4())
    
    user_data = {
        "user_id": user_id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    users_db[user_id] = user_data
    
    return {
        "message": "User created successfully",
        "user_id": user_id,
        "user": user_data
    }

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user by ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    return users_db[user_id]

@app.put("/users/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    """Update user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    if user.email:
        users_db[user_id]["email"] = user.email
    if user.full_name:
        users_db[user_id]["full_name"] = user.full_name
    
    users_db[user_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": "User updated successfully",
        "user": users_db[user_id]
    }

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user = users_db.pop(user_id)
    
    return {
        "message": "User deleted successfully",
        "user_id": user_id,
        "user": deleted_user
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)