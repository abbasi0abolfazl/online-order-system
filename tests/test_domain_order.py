import unittest
from datetime import datetime
from src.domain.entities.order import Order, OrderItem, OrderStatus
from src.domain.value_objects.address import Address


class TestOrderDomain(unittest.TestCase):
    """Test suite for Order Aggregate and Domain Entity business rules"""

    def setUp(self):
        self.item1 = OrderItem(
            product_id="prod_01",
            product_name="Mechanical Keyboard",
            quantity=1,
            unit_price=120.0
        )
        self.item2 = OrderItem(
            product_id="prod_02",
            product_name="Gaming Mouse",
            quantity=2,
            unit_price=45.0
        )

    def test_order_item_total_calculation(self):
        self.assertEqual(self.item1.total_price, 120.0)
        self.assertEqual(self.item2.total_price, 90.0)

    def test_order_item_validation_negative_quantity(self):
        with self.assertRaises(ValueError):
            OrderItem(
                product_id="prod_fail",
                product_name="Fail",
                quantity=0,
                unit_price=10.0
            )

    def test_order_item_validation_negative_price(self):
        with self.assertRaises(ValueError):
            OrderItem(
                product_id="prod_fail",
                product_name="Fail",
                quantity=1,
                unit_price=-5.0
            )

    def test_order_creation_and_total_calculation(self):
        order = Order(
            order_id="ord_100",
            customer_id="cust_01",
            items=[self.item1, self.item2]
        )
        self.assertEqual(order.status, OrderStatus.PENDING)
        self.assertEqual(order.total_amount, 210.0)
        self.assertEqual(len(order.items), 2)

    def test_order_empty_items_validation(self):
        with self.assertRaises(ValueError):
            Order(order_id="ord_empty", customer_id="cust_01", items=[])

    def test_order_status_transition(self):
        order = Order(
            order_id="ord_101",
            customer_id="cust_02",
            items=[self.item1]
        )
        self.assertEqual(order.status, OrderStatus.PENDING)
        order.update_status(OrderStatus.CONFIRMED)
        self.assertEqual(order.status, OrderStatus.CONFIRMED)
        order.update_status(OrderStatus.SHIPPED)
        self.assertEqual(order.status, OrderStatus.SHIPPED)

    def test_order_add_and_remove_items(self):
        order = Order(
            order_id="ord_102",
            customer_id="cust_03",
            items=[self.item1]
        )
        self.assertEqual(order.total_amount, 120.0)

        # Add item
        order.add_item(self.item2)
        self.assertEqual(order.total_amount, 210.0)
        self.assertEqual(len(order.items), 2)

        # Remove item
        order.remove_item("prod_01")
        self.assertEqual(order.total_amount, 90.0)
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.items[0].product_id, "prod_02")


class TestAddressValueObject(unittest.TestCase):
    """Test suite for Address Value Object"""

    def test_address_creation(self):
        addr = Address(
            street="Valiasr Ave",
            city="Tehran",
            postal_code="1234567890",
            country="Iran",
            apartment="Unit 12"
        )
        self.assertEqual(addr.city, "Tehran")
        self.assertEqual(addr.country, "Iran")
        self.assertEqual(addr.apartment, "Unit 12")

    def test_address_validation_empty_field(self):
        with self.assertRaises(ValueError):
            Address(
                street="",
                city="Tehran",
                postal_code="1234567890",
                country="Iran"
            )


if __name__ == "__main__":
    unittest.main()
