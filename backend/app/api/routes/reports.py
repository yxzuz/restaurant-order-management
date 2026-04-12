from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user, require_owner
from app.db import get_db
from app.services.report_service import ReportService
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/daily-sales")
def get_daily_sales(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner)
):
    """Get daily sales summary for the past N days (owner only)"""
    report_service = ReportService(db)
    return {
        "daily_sales": report_service.get_daily_sales_summary(days),
        "overall_stats": report_service.get_overall_stats(),
        "orders_by_status": report_service.get_orders_by_status()
    }


@router.get("/top-items")
def get_top_items(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner)
):
    """Get top selling menu items (owner only)"""
    report_service = ReportService(db)
    return {
        "top_items": report_service.get_top_selling_items(limit),
        "revenue_by_category": report_service.get_revenue_by_category()
    }


@router.get("/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner)
):
    """Get comprehensive analytics dashboard data (owner only)"""
    report_service = ReportService(db)

    return {
        "overall_stats": report_service.get_overall_stats(),
        "daily_sales": report_service.get_daily_sales_summary(days=7),
        "top_items": report_service.get_top_selling_items(limit=10),
        "revenue_by_category": report_service.get_revenue_by_category(),
        "orders_by_status": report_service.get_orders_by_status(),
        "hourly_distribution": report_service.get_hourly_distribution()
    }
