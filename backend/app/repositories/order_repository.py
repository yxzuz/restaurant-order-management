from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, *, status: OrderStatus = OrderStatus.NEW) -> Order:
        order = Order(status=status)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> Order | None:
        return (
            self.db.query(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.menu_item))
            .filter(Order.id == order_id)
            .first()
        )

    def list_all(self) -> list[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.items).joinedload(OrderItem.menu_item))
            .all()
        )

    def update_status(self, order: Order, status: OrderStatus) -> Order:
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete(self, order: Order) -> None:
        self.db.delete(order)
        self.db.commit()

    def add_item(
        self,
        *,
        order_id: int,
        menu_item_id: int,
        quantity: int,
        unit_price,
    ) -> OrderItem:
        item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
