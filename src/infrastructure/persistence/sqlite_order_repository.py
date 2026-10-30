import sqlite3
from typing import List, Optional
import json
from datetime import datetime
from ...domain.entities.order import Order, OrderItem, OrderStatus
from ...domain.repositories.order_repository import OrderRepository


class SQLiteOrderRepository(OrderRepository):
    """Repository implementation with SQLite"""
    
    def __init__(self, db_path: str = "orders.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
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
    
    def save(self, order: Order) -> Order:
        with sqlite3.connect(self.db_path) as conn:
            items_json = json.dumps([
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price
                }
                for item in order.items
            ])
            
            conn.execute("""
                INSERT INTO orders 
                (order_id, customer_id, status, total_amount, items, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                order.order_id,
                order.customer_id,
                order.status.value,
                order.total_amount,
                items_json,
                order.created_at.isoformat(),
                order.updated_at.isoformat()
            ))
            conn.commit()
        
        return order
    
    def find_by_id(self, order_id: str) -> Optional[Order]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM orders WHERE order_id = ?
            """, (order_id,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return self._row_to_order(row)
    
    def find_by_customer_id(self, customer_id: str) -> List[Order]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC
            """, (customer_id,))
            
            rows = cursor.fetchall()
            
            return [self._row_to_order(row) for row in rows]
    
    def update(self, order: Order) -> Order:
        with sqlite3.connect(self.db_path) as conn:
            items_json = json.dumps([
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price
                }
                for item in order.items
            ])
            
            conn.execute("""
                UPDATE orders SET
                status = ?,
                total_amount = ?,
                items = ?,
                updated_at = ?
                WHERE order_id = ?
            """, (
                order.status.value,
                order.total_amount,
                items_json,
                order.updated_at.isoformat(),
                order.order_id
            ))
            conn.commit()
        
        return order
    
    def delete(self, order_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
            conn.commit()
            
            return cursor.rowcount > 0
    
    def find_by_status(self, status: str) -> List[Order]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC
            """, (status,))
            
            rows = cursor.fetchall()
            
            return [self._row_to_order(row) for row in rows]
    
    def _row_to_order(self, row) -> Order:
        """Convert database row to Order object (Factory Method)"""
        items_data = json.loads(row[4])  # items column
        order_items = [
            OrderItem(
                product_id=item["product_id"],
                product_name=item["product_name"],
                quantity=item["quantity"],
                unit_price=item["unit_price"]
            )
            for item in items_data
        ]
        
        return Order(
            order_id=row[0],
            customer_id=row[1],
            status=OrderStatus(row[2]),
            items=order_items,
            created_at=datetime.fromisoformat(row[5]),
            updated_at=datetime.fromisoformat(row[6])
        )