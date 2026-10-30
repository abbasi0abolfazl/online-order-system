#!/bin/bash

echo "🚀 Starting all microservices..."
echo "========================================"

# Kill existing processes
echo "🛑 Stopping existing services..."
pkill -f "uvicorn" 2>/dev/null || true
sleep 2

# Start Order Service
echo "📦 Starting Order Service on port 8001..."
cd /home/abolfazl/workSpace/code/online-order-system/src
python -m uvicorn api.main:app --host 0.0.0.0 --port 8001 &
ORDER_PID=$!
echo "✅ Order Service started (PID: $ORDER_PID)"
sleep 3

# Start User Service
echo "👤 Starting User Service on port 8002..."
cd /home/abolfazl/workSpace/code/online-order-system/user-service/src
python -m uvicorn api.main:app --host 0.0.0.0 --port 8002 &
USER_PID=$!
echo "✅ User Service started (PID: $USER_PID)"
sleep 3

# Start API Gateway
echo "🌐 Starting API Gateway on port 8000..."
cd /home/abolfazl/workSpace/code/online-order-system/api-gateway
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
GATEWAY_PID=$!
echo "✅ API Gateway started (PID: $GATEWAY_PID)"
sleep 3

echo ""
echo "🎉 All services started successfully!"
echo ""
echo "🌐 Access URLs:"
echo "   Order Service:   http://localhost:8001"
echo "   Order Docs:      http://localhost:8001/docs"
echo "   User Service:    http://localhost:8002"
echo "   User Docs:       http://localhost:8002/docs"
echo "   API Gateway:     http://localhost:8000"
echo "   Gateway Docs:    http://localhost:8000/docs"
echo ""
echo "🔧 Quick Test Commands:"
echo "   curl http://localhost:8000/health"
echo "   curl http://localhost:8001/health"
echo "   curl http://localhost:8002/health"
echo ""
echo "🛑 Press Enter to stop all services..."
read

echo "⏹️ Stopping services..."
kill $ORDER_PID $USER_PID $GATEWAY_PID 2>/dev/null
echo "✅ All services stopped"