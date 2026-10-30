#!/usr/bin/env python3
"""
Comprehensive API Test Script
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_response(response, description=""):
    """Print formatted response"""
    print(f"\n{'='*60}")
    if description:
        print(f"📋 {description}")
    print(f"URL: {response.url}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2) if response.content else 'Empty'}")
    print('='*60)

def test_health():
    """Test health endpoints"""
    print("\n🧪 Testing Health Endpoints")
    
    # Test API Gateway health
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "API Gateway Health")
    
    # Test Order Service directly
    response = requests.get("http://localhost:8001/health")
    print_response(response, "Order Service Health (Direct)")
    
    # Test User Service directly
    response = requests.get("http://localhost:8002/health")
    print_response(response, "User Service Health (Direct)")

def test_crud_operations():
    """Test full CRUD operations"""
    print("\n🔄 Testing CRUD Operations")
    
    # 1. CREATE - Create new order
    order_data = {
        "customer_id": "test_customer_001",
        "items": [
            {
                "product_id": "prod_100",
                "product_name": "Laptop",
                "quantity": 1,
                "unit_price": 1200.00
            },
            {
                "product_id": "prod_101",
                "product_name": "Mouse",
                "quantity": 2,
                "unit_price": 25.50
            }
        ],
        "shipping_address": {
            "street": "123 Test Street",
            "city": "Tehran",
            "postal_code": "12345",
            "country": "Iran"
        }
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    print_response(response, "CREATE Order")
    
    if response.status_code == 201:
        order_id = response.json()["order_id"]
        
        # 2. READ - Get the created order
        response = requests.get(f"{BASE_URL}/orders/{order_id}")
        print_response(response, "READ Order")
        
        # 3. UPDATE - Update order status
        update_data = {
            "status": "confirmed"
        }
        response = requests.put(f"{BASE_URL}/orders/{order_id}", json=update_data)
        print_response(response, "UPDATE Order Status")
        
        # 4. READ ALL - Get all orders
        response = requests.get(f"{BASE_URL}/orders/")
        print_response(response, "READ ALL Orders")
        
        # 5. FILTER - Get orders by customer
        response = requests.get(f"{BASE_URL}/orders/customer/test_customer_001")
        print_response(response, "GET Customer Orders")
        
        # 6. DELETE - Delete the order
        response = requests.delete(f"{BASE_URL}/orders/{order_id}")
        print_response(response, "DELETE Order")
        
        # 7. VERIFY DELETE - Try to get deleted order
        response = requests.get(f"{BASE_URL}/orders/{order_id}")
        print_response(response, "VERIFY Deleted Order (Should be 404)")

def test_user_service():
    """Test User Service through API Gateway"""
    print("\n👤 Testing User Service")
    
    # Get user
    response = requests.get(f"{BASE_URL}/users/test_user_001")
    print_response(response, "GET User")
    
    # Create user (if endpoint exists)
    user_data = {
        "username": "test_user",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        print_response(response, "CREATE User")
    except:
        print("User creation endpoint not implemented yet")

def test_error_handling():
    """Test error cases"""
    print("\n⚠️ Testing Error Handling")
    
    # Non-existent order
    response = requests.get(f"{BASE_URL}/orders/nonexistent_id")
    print_response(response, "GET Non-existent Order")
    
    # Invalid JSON
    response = requests.post(f"{BASE_URL}/orders/", data="invalid json")
    print_response(response, "POST Invalid JSON")
    
    # Invalid status
    response = requests.patch(f"{BASE_URL}/orders/123/status?status=invalid_status")
    print_response(response, "UPDATE with Invalid Status")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Comprehensive API Tests")
    print("="*60)
    
    try:
        test_health()
        time.sleep(1)
        
        test_crud_operations()
        time.sleep(1)
        
        test_user_service()
        time.sleep(1)
        
        test_error_handling()
        
        print("\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to services. Make sure they are running.")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")

if __name__ == "__main__":
    run_all_tests()