from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user, require_owner
from app.db import get_db
from app.models.user import User
from app.schemas.order import OrderRead
from app.schemas.table import TableAccessRead, TableCreate, TableRead
from app.schemas.menu_item import MenuItemRead
from app.services.order_service import OrderService
from app.services.table_service import TableService

router = APIRouter()


@router.get("/", response_model=list[TableRead])
def list_tables(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TableService(db)
    return service.list_tables(current_user.restaurant_id)


@router.get("/access-links", response_model=list[TableAccessRead])
def list_table_access_links(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    service = TableService(db)
    return service.list_tables(current_user.restaurant_id)


@router.post("/", response_model=TableAccessRead, status_code=status.HTTP_201_CREATED)
def create_table(
    payload: TableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    service = TableService(db)
    try:
        return service.create_table(payload.number, current_user.restaurant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{table_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    service = TableService(db)
    try:
        deleted = service.delete_table(table_number, current_user.restaurant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")


@router.get("/{table_number}/active-order", response_model=OrderRead | None)
def get_active_order_for_table(
    table_number: int,
    qr_token: str = Query(...),
    db: Session = Depends(get_db),
):
    service = OrderService(db)
    try:
        return service.get_active_order_for_table(table_number, qr_token)
    except (LookupError, PermissionError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{table_number}/menu", response_model=list[MenuItemRead])
def get_menu_for_table(
    table_number: int,
    qr_token: str = Query(...),
    db: Session = Depends(get_db),
):
    """Public endpoint for customers to get menu via QR code"""
    from app.services.menu_service import MenuService
    from app.repositories.table_repository import TableRepository
    
    # Validate table access via QR token
    table_repo = TableRepository(db)
    table = table_repo.get_by_number_and_qr_token(table_number, qr_token)
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid table number or QR token"
        )
    
    # Return menu for this table's restaurant
    menu_service = MenuService(db)
    return menu_service.list_menu_items(table.restaurant_id)
