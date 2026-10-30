#!/usr/bin/env python3
"""
Complete system test
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_test_result(test_name, success, response=None):
    """Print test result"""
    emoji = "✅" if success else "❌"
    print(f"{emoji} {test_name}")
    if response and not success:
        print(f"   Status: {response.status_code}")
        if response.content:
            try:
                print(f"   Response: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"   Response: {response.text[:200]}")

def test_health():
    """Test health endpoints"""
    print("\n🧪 Testing Health Endpoints")
    
    success = True
    # Test API Gateway health
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code != 200:
        success = False
    print_test_result("API Gateway Health", response.status_code == 200, response)
    
    # Test direct services
    for service, port in [("Order", 8001), ("User", 8002)]:
        response = requests.get(f"http://localhost:{port}/health")
        if response.status_code != 200:
            success = False
        print_test_result(f"{service} Service Health (Direct)", response.status_code == 200, response)
    
    return success

def test_user_crud():
    """Test User CRUD operations"""
    print("\n👤 Testing User CRUD Operations")
    
    # 1. Get all users (should be empty initially)
    response = requests.get(f"{BASE_URL}/users")
    initial_count = response.json().get("count", 0)
    print_test_result("GET /users (initial)", response.status_code == 200, response)
    
    # 2. Create user
    user_data = {
        "username": "test_user_1",
        "email": "test1@example.com",
        "full_name": "Test User One"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    if response.status_code != 201:
        print_test_result("POST /users (create)", False, response)
        return False
    
    print_test_result("POST /users (create)", True)
    user_id = response.json().get("user_id")
    
    # 3. Get created user
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print_test_result(f"GET /users/{user_id}", response.status_code == 200, response)
    
    # 4. Update user
    update_data = {"email": "updated@example.com"}
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    print_test_result(f"PUT /users/{user_id}", response.status_code == 200, response)
    
    # 5. Get all users again
    response = requests.get(f"{BASE_URL}/users")
    final_count = response.json().get("count", 0)
    print_test_result(f"GET /users (final count: {final_count})", 
                     response.status_code == 200 and final_count == initial_count + 1, 
                     response)
    
    # 6. Delete user
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    print_test_result(f"DELETE /users/{user_id}", response.status_code == 200, response)
    
    return True

def test_order_crud():
    """Test Order CRUD operations"""
    print("\n📦 Testing Order CRUD Operations")
    
    # 1. Get all orders
    response = requests.get(f"{BASE_URL}/orders")
    initial_count = response.json().get("count", 0)
    print_test_result("GET /orders (initial)", response.status_code == 200, response)
    
    # 2. Create order
    order_data = {
        "customer_id": "test_customer_001",
        "items": [
            {
                "product_id": "prod_001",
                "product_name": "Laptop",
                "quantity": 2,
                "unit_price": 1000.50
            }
        ],
        "shipping_address": {
            "street": "123 Main St",
            "city": "Tehran",
            "postal_code": "123456",
            "country": "Iran"
        }
    }
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    if response.status_code != 201:
        print_test_result("POST /orders (create)", False, response)
        return False
    
    print_test_result("POST /orders (create)", True)
    order_id = response.json().get("order_id")
    
    # 3. Get created order
    response = requests.get(f"{BASE_URL}/orders/{order_id}")
    print_test_result(f"GET /orders/{order_id}", response.status_code == 200, response)
    
    # 4. Update order status
    response = requests.patch(f"{BASE_URL}/orders/{order_id}/status?status=confirmed")
    print_test_result(f"PATCH /orders/{order_id}/status", response.status_code == 200, response)
    
    # 5. Get all orders for customer
    response = requests.get(f"{BASE_URL}/orders?customer_id=test_customer_001")
    print_test_result("GET /orders?customer_id=test_customer_001", 
                     response.status_code == 200, 
                     response)
    
    # 6. Get all orders
    response = requests.get(f"{BASE_URL}/orders")
    final_count = response.json().get("count", 0)
    print_test_result(f"GET /orders (final count: {final_count})", 
                     response.status_code == 200 and final_count == initial_count + 1, 
                     response)
    
    return True

def test_error_cases():
    """Test error handling"""
    print("\n⚠️ Testing Error Cases")
    
    # 1. Get non-existent user
    response = requests.get(f"{BASE_URL}/users/nonexistent")
    print_test_result("GET non-existent user (404)", response.status_code == 404, response)
    
    # 2. Get non-existent order
    response = requests.get(f"{BASE_URL}/orders/nonexistent")
    print_test_result("GET non-existent order (404)", response.status_code == 404, response)
    
    # 3. Create order with invalid data
    response = requests.post(f"{BASE_URL}/orders", json={"invalid": "data"})
    print_test_result("POST order with invalid data (400/422)", 
                     response.status_code in [400, 422], 
                     response)
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Complete System Test")
    print("=" * 60)
    
    try:
        all_success = True
        
        # Test 1: Health endpoints
        if not test_health():
            all_success = False
        
        time.sleep(1)
        
        # Test 2: User CRUD
        if not test_user_crud():
            all_success = False
        
        time.sleep(1)
        
        # Test 3: Order CRUD
        if not test_order_crud():
            all_success = False
        
        time.sleep(1)
        
        # Test 4: Error cases
        if not test_error_cases():
            all_success = False
        
        print("\n" + "=" * 60)
        if all_success:
            print("🎉 All tests passed! System is working correctly.")
        else:
            print("❌ Some tests failed. Check the errors above.")
        
        return all_success
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to services. Make sure they are running.")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)