from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderStatus, PaymentStatus
from app.models.order_item import OrderItem


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(
        self,
        *,
        table_id: int,
        status: OrderStatus = OrderStatus.NEW,
        payment_status: PaymentStatus = PaymentStatus.UNPAID,
    ) -> Order:
        order = Order(table_id=table_id, status=status, payment_status=payment_status)
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

    def list_all(self) -> list[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.table), joinedload(Order.items).joinedload(OrderItem.menu_item))
            .order_by(Order.created_at.desc())
            .all()
        )

    def list_active(self) -> list[Order]:
        return (
            self.db.query(Order)
            .options(joinedload(Order.table), joinedload(Order.items).joinedload(OrderItem.menu_item))
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
