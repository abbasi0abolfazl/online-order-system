from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI(
    title="API Gateway",
    description="Gateway for Order Management System",
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

# Service URLs
SERVICE_URLS = {
    "order": "http://localhost:8001",
    "user": "http://localhost:8002"
}

def get_request_body(request: Request):
    """Get request body as JSON or raw"""
    try:
        return request.json()
    except:
        return None

async def forward_request(service_name: str, path: str, request: Request):
    """Forward request to appropriate service"""
    if service_name not in SERVICE_URLS:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    target_url = f"{SERVICE_URLS[service_name]}/{path}"
    
    try:
        # Get request body if exists
        body = None
        content_type = request.headers.get("content-type", "")
        
        if request.method in ["POST", "PUT", "PATCH"] and "application/json" in content_type:
            try:
                body = await request.json()
            except:
                body = await request.body()
        elif request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
        
        # Forward the request
        response = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for key, value in request.headers.items() 
                    if key.lower() not in ['host', 'content-length']},
            params=dict(request.query_params),
            json=body if isinstance(body, dict) else None,
            data=body if not isinstance(body, dict) else None,
            timeout=10
        )
        
        return JSONResponse(
            content=response.json() if response.content else {},
            status_code=response.status_code
        )
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail=f"Service {service_name} is unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    """Health check for API Gateway and all services"""
    services_health = {}
    
    for service_name, url in SERVICE_URLS.items():
        try:
            response = requests.get(f"{url}/health", timeout=2)
            services_health[service_name] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "status_code": response.status_code
            }
        except requests.exceptions.RequestException as e:
            services_health[service_name] = {
                "status": "unreachable",
                "error": str(e)
            }
    
    return {
        "gateway": "healthy",
        "services": services_health
    }

# Order Service routes
@app.api_route("/orders", methods=["GET", "POST"])
@app.api_route("/orders/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_orders(path: str = "", request: Request = None):
    """Proxy order service requests"""
    full_path = f"orders/{path}" if path else "orders"
    return await forward_request("order", full_path, request)

# User Service routes  
@app.api_route("/users", methods=["GET", "POST"])
@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_users(path: str = "", request: Request = None):
    """Proxy user service requests"""
    full_path = f"users/{path}" if path else "users"
    return await forward_request("user", full_path, request)

# Direct service access (for debugging)
@app.api_route("/service/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def service_proxy(service_name: str, path: str, request: Request):
    """Generic service proxy"""
    return await forward_request(service_name, path, request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)