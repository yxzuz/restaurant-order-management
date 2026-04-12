from datetime import datetime, timedelta
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus, PaymentStatus
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.core.timezone import now_thai


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_daily_sales_summary(self, days: int = 7):
        """Get daily sales summary for the past N days"""
        end_date = now_thai()
        start_date = end_date - timedelta(days=days)

        # Daily revenue from paid orders
        daily_sales = (
            self.db.query(
                func.date(Order.created_at).label('date'),
                func.sum(Order.total_amount).label('revenue'),
                func.count(Order.id).label('order_count')
            )
            .filter(Order.payment_status == PaymentStatus.PAID)
            .filter(Order.created_at >= start_date)
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at).desc())
            .all()
        )

        return [
            {
                'date': str(record.date),
                'revenue': float(record.revenue or 0),
                'order_count': record.order_count
            }
            for record in daily_sales
        ]

    def get_overall_stats(self):
        """Get overall statistics"""
        # Total revenue from paid orders
        total_revenue = (
            self.db.query(func.sum(Order.total_amount))
            .filter(Order.payment_status == PaymentStatus.PAID)
            .scalar() or 0
        )

        # Total orders
        total_orders = self.db.query(func.count(Order.id)).scalar() or 0

        # Paid orders count
        paid_orders = (
            self.db.query(func.count(Order.id))
            .filter(Order.payment_status == PaymentStatus.PAID)
            .scalar() or 0
        )

        # Pending orders (unpaid, not cancelled)
        pending_orders = (
            self.db.query(func.count(Order.id))
            .filter(Order.payment_status == PaymentStatus.UNPAID)
            .filter(Order.status != OrderStatus.CANCELLED)
            .scalar() or 0
        )

        # Average order value (from paid orders)
        avg_order_value = float(total_revenue) / \
            paid_orders if paid_orders > 0 else 0

        return {
            'total_revenue': float(total_revenue),
            'total_orders': total_orders,
            'paid_orders': paid_orders,
            'pending_orders': pending_orders,
            'avg_order_value': round(avg_order_value, 2)
        }

    def get_orders_by_status(self):
        """Get order counts grouped by status"""
        status_counts = (
            self.db.query(
                Order.status,
                func.count(Order.id).label('count')
            )
            .group_by(Order.status)
            .all()
        )

        return [
            {
                'status': record.status.value,
                'count': record.count
            }
            for record in status_counts
        ]

    def get_top_selling_items(self, limit: int = 10):
        """Get top selling menu items by quantity sold"""
        top_items = (
            self.db.query(
                MenuItem.id,
                MenuItem.name,
                MenuItem.price,
                MenuItem.category,
                func.sum(OrderItem.quantity).label('total_quantity'),
                func.sum(OrderItem.subtotal).label('total_revenue'),
                func.count(OrderItem.id).label('order_count')
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(Order.payment_status == PaymentStatus.PAID)
            .group_by(MenuItem.id, MenuItem.name, MenuItem.price, MenuItem.category)
            .order_by(desc(func.sum(OrderItem.quantity)))
            .limit(limit)
            .all()
        )

        return [
            {
                'id': record.id,
                'name': record.name,
                'price': float(record.price),
                'category': record.category,
                'total_quantity': record.total_quantity,
                'total_revenue': float(record.total_revenue or 0),
                'order_count': record.order_count
            }
            for record in top_items
        ]

    def get_revenue_by_category(self):
        """Get revenue breakdown by menu category"""
        category_revenue = (
            self.db.query(
                MenuItem.category,
                func.sum(OrderItem.subtotal).label('revenue'),
                func.sum(OrderItem.quantity).label('quantity')
            )
            .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(Order.payment_status == PaymentStatus.PAID)
            .group_by(MenuItem.category)
            .order_by(desc(func.sum(OrderItem.subtotal)))
            .all()
        )

        return [
            {
                'category': record.category,
                'revenue': float(record.revenue or 0),
                'quantity': record.quantity
            }
            for record in category_revenue
        ]

    def get_hourly_distribution(self):
        """Get order distribution by hour of day"""
        hourly_orders = (
            self.db.query(
                func.extract('hour', Order.created_at).label('hour'),
                func.count(Order.id).label('order_count'),
                func.sum(Order.total_amount).label('revenue')
            )
            .filter(Order.payment_status == PaymentStatus.PAID)
            .group_by(func.extract('hour', Order.created_at))
            .order_by(func.extract('hour', Order.created_at))
            .all()
        )

        return [
            {
                'hour': int(record.hour),
                'order_count': record.order_count,
                'revenue': float(record.revenue or 0)
            }
            for record in hourly_orders
        ]
