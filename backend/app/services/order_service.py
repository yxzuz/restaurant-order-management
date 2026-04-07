from app.models.order import OrderStatus, PaymentStatus
from app.models.table import TableStatus
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.table_repository import TableRepository


ALLOWED_STATUS_TRANSITIONS = {
    OrderStatus.NEW: {OrderStatus.PREPARING, OrderStatus.CANCELLED},
    OrderStatus.PREPARING: {OrderStatus.READY},
    OrderStatus.READY: {OrderStatus.COMPLETED},
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELLED: set(),
}


class OrderService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.order_repository = OrderRepository(db_session)
        self.menu_item_repository = MenuItemRepository(db_session)
        self.table_repository = TableRepository(db_session)

    def list_orders(self):
        return self.order_repository.list_all()

    def list_active_orders(self):
        return self.order_repository.list_active()

    def create_order(self, order_data):
        table = self._get_table_by_access(order_data["table_number"], order_data["qr_token"])

        order = self.order_repository.get_active_by_table_id(table.id)
        if order is None:
            order = self.order_repository.create_order(table_id=table.id)
            self.table_repository.update_status(table, TableStatus.OCCUPIED)

        for item_data in order_data.get("items", []):
            menu_item = self.menu_item_repository.get_by_id(item_data["menu_item_id"])
            if menu_item is None:
                raise ValueError(f"Menu item {item_data['menu_item_id']} not found")
            if not menu_item.is_available:
                raise ValueError(f"Menu item {item_data['menu_item_id']} is unavailable")

            self.order_repository.add_item(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=item_data["quantity"],
                unit_price=menu_item.price,
            )

        return self.order_repository.get_by_id(order.id)

    def get_order(self, order_id):
        return self.order_repository.get_by_id(order_id)

    def get_active_order_for_table(self, table_number: int, qr_token: str):
        table = self._get_table_by_access(table_number, qr_token)
        return self.order_repository.get_active_by_table_id(table.id)

    def update_order_status(self, order_id, new_status):
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            return None

        status = new_status if isinstance(new_status, OrderStatus) else OrderStatus(new_status)
        if status not in ALLOWED_STATUS_TRANSITIONS[order.status]:
            raise ValueError(f"Invalid status transition: {order.status.value} -> {status.value}")
        return self.order_repository.update_status(order, status)

    def update_payment_status(self, order_id, payment_status):
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            return None

        status = (
            payment_status
            if isinstance(payment_status, PaymentStatus)
            else PaymentStatus(payment_status)
        )

        if status == PaymentStatus.PAID and order.status not in {OrderStatus.READY, OrderStatus.COMPLETED}:
            raise ValueError("Order can be marked as paid only when it is ready or completed")

        updated_order = self.order_repository.update_payment_status(order, status)
        if status == PaymentStatus.PAID:
            self.table_repository.update_status(order.table, TableStatus.AVAILABLE)
        return updated_order

    def delete_order(self, order_id):
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            return False

        self.order_repository.delete(order)
        return True

    def _get_table_by_access(self, table_number: int, qr_token: str):
        table = self.table_repository.get_by_number(table_number)
        if table is None:
            raise LookupError(f"Table {table_number} not found")

        matched_table = self.table_repository.get_by_number_and_qr_token(table_number, qr_token)
        if matched_table is None:
            raise PermissionError("Invalid QR token for table")

        return matched_table
