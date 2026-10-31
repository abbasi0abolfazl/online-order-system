import unittest
from unittest.mock import MagicMock
from src.domain.entities.order import Order, OrderItem, OrderStatus
from src.application.commands.create_order_command import CreateOrderCommand, OrderItemDTO
from src.application.commands.update_order_command import UpdateOrderStatusCommand
from src.application.command_handlers.order_command_handler import OrderCommandHandler


class TestOrderCommandHandler(unittest.TestCase):
    """Test suite for Application layer Command Handlers"""

    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_event_publisher = MagicMock()
        self.handler = OrderCommandHandler(
            repository=self.mock_repo,
            event_publisher=self.mock_event_publisher
        )

    def test_handle_create_order(self):
        # Setup command DTO
        item_dto = OrderItemDTO(
            product_id="prod_101",
            product_name="Wireless Keyboard",
            quantity=2,
            unit_price=50.0
        )
        command = CreateOrderCommand(
            customer_id="cust_999",
            items=[item_dto],
            shipping_address={"street": "123 Main St", "city": "Tehran", "postal_code": "123456", "country": "Iran"}
        )

        # Mock repo save behavior
        def mock_save(order):
            return order
        self.mock_repo.save.side_effect = mock_save

        # Execute
        result = self.handler.handle_create_order(command)

        # Assertions
        self.assertIn("order_id", result)
        self.assertEqual(result["status"], OrderStatus.PENDING.value)
        self.assertEqual(result["total_amount"], 100.0)
        self.mock_repo.save.assert_called_once()
        self.mock_event_publisher.publish_order_created.assert_called_once()

    def test_handle_update_order_status(self):
        existing_order = Order(
            order_id="ord_exist",
            customer_id="cust_888",
            items=[OrderItem("prod_1", "Item", 1, 20.0)],
            status=OrderStatus.PENDING
        )
        self.mock_repo.find_by_id.return_value = existing_order
        self.mock_repo.update.return_value = existing_order

        command = UpdateOrderStatusCommand(
            order_id="ord_exist",
            new_status=OrderStatus.SHIPPED
        )

        result = self.handler.handle_update_order_status(command)

        self.assertEqual(result["new_status"], OrderStatus.SHIPPED.value)
        self.mock_repo.find_by_id.assert_called_once_with("ord_exist")
        self.mock_repo.update.assert_called_once()
        self.mock_event_publisher.publish_order_status_changed.assert_called_once()

    def test_handle_update_order_status_not_found(self):
        self.mock_repo.find_by_id.return_value = None
        command = UpdateOrderStatusCommand(
            order_id="ord_non_existent",
            new_status=OrderStatus.DELIVERED
        )

        with self.assertRaises(ValueError):
            self.handler.handle_update_order_status(command)


if __name__ == "__main__":
    unittest.main()
