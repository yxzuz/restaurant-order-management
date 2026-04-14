from datetime import datetime

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.models.order import Order, OrderStatus, PaymentStatus
from app.models.order_item import OrderItem


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_daily_sales_summary(self, restaurant_id: int, start_date: datetime):
        return (
            self.db.query(
                func.date(Order.created_at).label("date"),
                func.sum(OrderItem.quantity *
                         OrderItem.unit_price).label("revenue"),
                func.count(func.distinct(Order.id)).label("order_count"),
            )
            .join(OrderItem, OrderItem.order_id == Order.id)
            .filter(Order.payment_status == PaymentStatus.PAID)
            .filter(Order.restaurant_id == restaurant_id)
            .filter(Order.created_at >= start_date)
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at).desc())
            .all()
        )

    def get_total_revenue(self, restaurant_id: int):
        return (
            self.db.query(func.sum(OrderItem.quantity * OrderItem.unit_price))
            .join(Order, OrderItem.order_id == Order.id)
            .filter(Order.payment_status == PaymentStatus.PAID)
            .filter(Order.restaurant_id == restaurant_id)
            .scalar()
        )

    def count_orders(self, restaurant_id: int):
        return (
            self.db.query(func.count(Order.id))
            .filter(Order.restaurant_id == restaurant_id)
            .scalar()
        )

    def count_paid_orders(self, restaurant_id: int):
        return (
            self.db.query(func.count(Order.id))
            .filter(Order.payment_status == PaymentStatus.PAID)
            .filter(Order.restaurant_id == restaurant_id)
            .scalar()
        )

    def count_pending_orders(self, restaurant_id: int):
        return (
            self.db.query(func.count(Order.id))
            .filter(Order.payment_status == PaymentStatus.UNPAID)
            .filter(Order.status != OrderStatus.CANCELLED)
            .filter(Order.restaurant_id == restaurant_id)
            .scalar()
        )

    def get_orders_by_status(self, restaurant_id: int):
        return (
            self.db.query(Order.status, func.count(Order.id).label("count"))
            .filter(Order.restaurant_id == restaurant_id)
            .group_by(Order.status)
            .all()
        )

    def get_top_selling_items(self, restaurant_id: int, limit: int):
        return (
            self.db.query(
                MenuItem.id,
                MenuItem.name,
                MenuItem.price,
                MenuItem.category,
                func.sum(OrderItem.quantity).label("total_quantity"),
                func.sum(OrderItem.quantity *
                         OrderItem.unit_price).label("total_revenue"),
                func.count(func.distinct(Order.id)).label("order_count"),
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(Order.payment_status == PaymentStatus.PAID)
            .filter(Order.restaurant_id == restaurant_id)
            .filter(MenuItem.restaurant_id == restaurant_id)
            .group_by(MenuItem.id, MenuItem.name, MenuItem.price, MenuItem.category)
            .order_by(desc(func.sum(OrderItem.quantity)))
            .limit(limit)
            .all()
        )

    def get_revenue_by_category(self, restaurant_id: int):
        return (
            self.db.query(
                MenuItem.category,
                func.sum(OrderItem.quantity *
                         OrderItem.unit_price).label("revenue"),
                func.sum(OrderItem.quantity).label("quantity"),
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(Order.payment_status == PaymentStatus.PAID)
            .filter(Order.restaurant_id == restaurant_id)
            .filter(MenuItem.restaurant_id == restaurant_id)
            .group_by(MenuItem.category)
            .order_by(desc(func.sum(OrderItem.quantity * OrderItem.unit_price)))
            .all()
        )

    def get_hourly_distribution(self, restaurant_id: int):
        return (
            self.db.query(
                func.extract("hour", Order.created_at).label("hour"),
                func.count(func.distinct(Order.id)).label("order_count"),
                func.sum(OrderItem.quantity *
                         OrderItem.unit_price).label("revenue"),
            )
            .join(OrderItem, OrderItem.order_id == Order.id)
            .filter(Order.payment_status == PaymentStatus.PAID)
            .filter(Order.restaurant_id == restaurant_id)
            .group_by(func.extract("hour", Order.created_at))
            .order_by(func.extract("hour", Order.created_at))
            .all()
        )
