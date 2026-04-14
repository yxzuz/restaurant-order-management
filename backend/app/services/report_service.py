from datetime import timedelta
from sqlalchemy.orm import Session

from app.core.timezone import now_thai
from app.repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, db: Session, restaurant_id: int):
        self.report_repository = ReportRepository(db)
        self.restaurant_id = restaurant_id

    def get_daily_sales_summary(self, days: int = 7):
        """Get daily sales summary for the past N days"""
        end_date = now_thai()
        start_date = end_date - timedelta(days=days)

        daily_sales = self.report_repository.get_daily_sales_summary(
            self.restaurant_id,
            start_date,
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
        total_revenue = self.report_repository.get_total_revenue(self.restaurant_id) or 0
        total_orders = self.report_repository.count_orders(self.restaurant_id) or 0
        paid_orders = self.report_repository.count_paid_orders(self.restaurant_id) or 0
        pending_orders = self.report_repository.count_pending_orders(self.restaurant_id) or 0

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
        status_counts = self.report_repository.get_orders_by_status(self.restaurant_id)

        return [
            {
                'status': record.status.value,
                'count': record.count
            }
            for record in status_counts
        ]

    def get_top_selling_items(self, limit: int = 10):
        """Get top selling menu items by quantity sold"""
        top_items = self.report_repository.get_top_selling_items(
            self.restaurant_id,
            limit,
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
        category_revenue = self.report_repository.get_revenue_by_category(
            self.restaurant_id,
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
        hourly_orders = self.report_repository.get_hourly_distribution(
            self.restaurant_id,
        )

        return [
            {
                'hour': int(record.hour),
                'order_count': record.order_count,
                'revenue': float(record.revenue or 0)
            }
            for record in hourly_orders
        ]
