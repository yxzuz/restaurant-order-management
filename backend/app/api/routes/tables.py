from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.order import OrderRead
from app.schemas.table import TableRead
from app.services.order_service import OrderService
from app.services.table_service import TableService

router = APIRouter()


@router.get("/", response_model=list[TableRead])
def list_tables(db: Session = Depends(get_db)):
    service = TableService(db)
    return service.list_tables()


@router.get("/{table_number}/active-order", response_model=OrderRead | None)
def get_active_order_for_table(
    table_number: int,
    qr_token: str = Query(...),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    try:
        return service.get_active_order_for_table(table_number, qr_token)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
