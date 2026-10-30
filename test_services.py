#!/usr/bin/env python3
"""
Test if services are running
"""

import requests
import time

def test_service(name, url, timeout=5):
    """Test if a service is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name} is running at {url}")
            return True
        else:
            print(f"❌ {name} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {name} is not reachable: {e}")
        return False

def main():
    """Test all services"""
    services = [
        ("Order Service", "http://localhost:8001/health"),
        ("User Service", "http://localhost:8002/health"),
        ("API Gateway", "http://localhost:8000/health"),
    ]
    
    print("🧪 Testing services...")
    
    all_ok = True
    for name, url in services:
        if not test_service(name, url):
            all_ok = False
        time.sleep(1)
    
    if all_ok:
        print("\n🎉 All services are running!")
    else:
        print("\n⚠️  Some services are not running correctly")

if __name__ == "__main__":
    main()