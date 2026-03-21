from app.models.order import OrderStatus
from app.repositories.menu_item_repository import MenuItemRepository
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.order_repository = OrderRepository(db_session)
        self.menu_item_repository = MenuItemRepository(db_session)

    def list_orders(self):
        return self.order_repository.list_all()

    def create_order(self, order_data):
        order = self.order_repository.create_order()

        for item_data in order_data.get("items", []):
            menu_item = self.menu_item_repository.get_by_id(item_data["menu_item_id"])
            if menu_item is None:
                raise ValueError(f"Menu item {item_data['menu_item_id']} not found")

            self.order_repository.add_item(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=item_data["quantity"],
                unit_price=menu_item.price,
            )

        return self.order_repository.get_by_id(order.id)

    def get_order(self, order_id):
        return self.order_repository.get_by_id(order_id)

    def update_order_status(self, order_id, new_status):
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            return None

        status = new_status if isinstance(new_status, OrderStatus) else OrderStatus(new_status)
        return self.order_repository.update_status(order, status)

    def delete_order(self, order_id):
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            return False

        self.order_repository.delete(order)
        return True
