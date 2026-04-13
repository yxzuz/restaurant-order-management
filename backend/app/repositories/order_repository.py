from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderStatus, PaymentStatus
from app.models.order_item import OrderItem, ItemStatus


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(
        self,
        *,
        table_id: int,
        restaurant_id: int,
        status: OrderStatus = OrderStatus.NEW,
        payment_status: PaymentStatus = PaymentStatus.UNPAID,
    ) -> Order:
        order = Order(table_id=table_id, restaurant_id=restaurant_id, status=status,
                      payment_status=payment_status)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_by_id(self, order_id: int) -> Order | None:
        return (
            self.db.query(Order)
            .options(joinedload(Order.table), joinedload(Order.items).joinedload(OrderItem.menu_item))
            .filter(Order.id == order_id)
            .first()
        )

    def list_all(self, restaurant_id: int) -> list[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.table), joinedload(Order.items).joinedload(OrderItem.menu_item))
            .filter(Order.restaurant_id == restaurant_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def list_active(self, restaurant_id: int) -> list[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.table), joinedload(Order.items).joinedload(OrderItem.menu_item))
            .filter(Order.restaurant_id == restaurant_id)
            .filter(Order.payment_status == PaymentStatus.UNPAID)
            .filter(Order.status != OrderStatus.CANCELLED)
            .order_by(Order.created_at.asc())
            .all()
        )

    def get_active_by_table_id(self, table_id: int) -> Order | None:
        return (
            self.db.query(Order)
            .options(joinedload(Order.table), joinedload(Order.items).joinedload(OrderItem.menu_item))
            .filter(Order.table_id == table_id)
            .filter(Order.payment_status == PaymentStatus.UNPAID)
            .filter(Order.status != OrderStatus.CANCELLED)
            .order_by(Order.created_at.desc())
            .first()
        )

    def has_orders_for_table_id(self, table_id: int) -> bool:
        return self.db.query(Order.id).filter(Order.table_id == table_id).first() is not None

    def update_status(self, order: Order, status: OrderStatus) -> Order:
        order.status = status
        order.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_payment_status(self, order: Order, payment_status: PaymentStatus) -> Order:
        order.payment_status = payment_status
        order.updated_at = datetime.utcnow()
        if payment_status == PaymentStatus.PAID:
            order.closed_at = datetime.utcnow()
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

    def get_order_item(self, order_id: int, item_id: int) -> OrderItem | None:
        return (
            self.db.query(OrderItem)
            .filter(OrderItem.order_id == order_id, OrderItem.id == item_id)
            .first()
        )

    def update_item_status(self, item: OrderItem, status: ItemStatus) -> OrderItem:
        item.status = status
        item.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_item(self, item: OrderItem) -> None:
        self.db.delete(item)
        self.db.commit()
