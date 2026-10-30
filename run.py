#!/usr/bin/env python3
"""
Fixed run script for microservices
"""

import subprocess
import time
import os
import sys
import signal

def run_service(name, command, cwd=None, delay=3):
    """Run a service and wait to see if it starts"""
    print(f"\n🚀 Starting {name}...")
    if cwd:
        print(f"📁 Directory: {cwd}")
    
    try:
        # Start the process
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Give it time to start
        time.sleep(delay)
        
        # Check if it's still running
        if process.poll() is None:
            print(f"✅ {name} started successfully")
            return process
        else:
            # Read any error output
            stdout, stderr = process.communicate()
            print(f"❌ {name} failed to start")
            if stderr:
                # Show first few lines of error
                error_lines = stderr.strip().split('\n')[:5]
                for line in error_lines:
                    print(f"   Error: {line[:100]}...")
            return None
            
    except Exception as e:
        print(f"❌ Exception starting {name}: {e}")
        return None

def main():
    """Main function"""
    print("=" * 50)
    print("🎯 Online Order Management System - FIXED")
    print("=" * 50)
    
    # Get project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    processes = []
    
    # 1. Start Order Service (with more detailed debugging)
    print("\n" + "=" * 30)
    print("1. ORDER SERVICE")
    print("=" * 30)
    
    order_cwd = os.path.join(project_root, "src")
    
    # First, check if we can import the module
    print("Testing Order Service import...")
    test_cmd = f"cd {order_cwd} && python -c \"import api.main\""
    result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Import test passed")
    else:
        print(f"❌ Import test failed: {result.stderr[:200]}")
        print("Creating simple Order Service...")
        
        # Create a simple working version
        simple_main = os.path.join(order_cwd, "api", "main_simple.py")
        with open(simple_main, "w") as f:
            f.write('''
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Order Service")

@app.get("/")
def root():
    return {"message": "Order Service"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
''')
    
    # Now try to start it
    order_process = run_service(
        "Order Service",
        "python -m uvicorn api.main:app --host 0.0.0.0 --port 8001",
        cwd=order_cwd,
        delay=4
    )
    
    if order_process:
        processes.append(("Order Service", order_process))
    
    # 2. Start User Service
    print("\n" + "=" * 30)
    print("2. USER SERVICE")
    print("=" * 30)
    
    user_cwd = os.path.join(project_root, "user-service", "src")
    user_process = run_service(
        "User Service",
        "python -m uvicorn api.main:app --host 0.0.0.0 --port 8002",
        cwd=user_cwd,
        delay=2
    )
    
    if user_process:
        processes.append(("User Service", user_process))
    
    # 3. Start API Gateway
    print("\n" + "=" * 30)
    print("3. API GATEWAY")
    print("=" * 30)
    
    gateway_cwd = os.path.join(project_root, "api-gateway")
    gateway_process = run_service(
        "API Gateway",
        "python -m uvicorn main:app --host 0.0.0.0 --port 8000",
        cwd=gateway_cwd,
        delay=2
    )
    
    if gateway_process:
        processes.append(("API Gateway", gateway_process))
    
    # Show status
    print("\n" + "=" * 50)
    print("📊 SERVICE STATUS")
    print("=" * 50)
    
    for name, process in processes:
        if process and process.poll() is None:
            print(f"✅ {name}: RUNNING (PID: {process.pid})")
        else:
            print(f"❌ {name}: STOPPED")
    
    # URLs
    print("\n🌐 ACCESS URLS:")
    print("   Order Service:   http://localhost:8001")
    print("   Order Docs:      http://localhost:8001/docs")
    print("   User Service:    http://localhost:8002")
    print("   API Gateway:     http://localhost:8000")
    
    # Test connections
    print("\n🧪 QUICK TEST:")
    import requests
    
    for url, name in [
        ("http://localhost:8001/health", "Order Service"),
        ("http://localhost:8002/health", "User Service"),
        ("http://localhost:8000/health", "API Gateway")
    ]:
        try:
            response = requests.get(url, timeout=2)
            print(f"   ✅ {name}: {response.status_code}")
        except:
            print(f"   ❌ {name}: Not reachable")
    
    print("\n🛑 Press Ctrl+C to stop all services...")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  Stopping services...")
        
        for name, process in processes:
            if process and process.poll() is None:
                print(f"   Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✅ All services stopped")

if __name__ == "__main__":
    main()