from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db import get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderPaymentUpdate, OrderRead, OrderUpdate
from app.schemas.order_item import OrderItemStatusUpdate
from app.services.auth_service import AuthService
from app.services.order_service import OrderService


def _get_optional_user(
    token: str | None,
    db: Session,
) -> User | None:
    if not token:
        return None
    service = AuthService(db)
    return service.get_current_user(token)


router = APIRouter()


@router.get("/", response_model=list[OrderRead])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    return service.list_orders(current_user.restaurant_id)


@router.get("/active", response_model=list[OrderRead])
def list_active_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    return service.list_active_orders(current_user.restaurant_id)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    order = service.get_order(order_id)
    if order is None or order.restaurant_id != current_user.restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    service = OrderService(db)
    try:
        return service.create_order(payload.model_dump())
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    payload: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.status is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status is required",
        )

    service = OrderService(db)
    existing = service.get_order(order_id)
    if existing is None or existing.restaurant_id != current_user.restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    try:
        order = service.update_order_status(order_id, payload.status)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{order_id}/payment", response_model=OrderRead)
def update_order_payment(
    order_id: int,
    payload: OrderPaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    existing = service.get_order(order_id)
    if existing is None or existing.restaurant_id != current_user.restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    try:
        order = service.update_payment_status(order_id, payload.payment_status)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{order_id}/items/{item_id}/status", response_model=OrderRead)
def update_order_item_status(
    order_id: int,
    item_id: int,
    payload: OrderItemStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    existing = service.get_order(order_id)
    if existing is None or existing.restaurant_id != current_user.restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order or item not found",
        )
    try:
        order = service.update_order_item_status(
            order_id, item_id, payload.status)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Order or item not found")
    return order


@router.delete("/{order_id}/items/{item_id}", response_model=OrderRead)
def cancel_order_item(
    order_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    qr_token: str | None = Query(None),
    authorization: str | None = Header(None),
):
    service = OrderService(db)
    existing = service.get_order(order_id)

    # Resolve optional JWT from Authorization header (if present)
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip() or None
    current_user = _get_optional_user(token, db)

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order or item not found",
        )

    if current_user is not None:
        # Staff/owner path: tenant-scoped
        if existing.restaurant_id != current_user.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order or item not found",
            )
    else:
        # Customer path: must prove table access via QR token
        if not qr_token or not existing.table or existing.table.qr_token != qr_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid table number or QR token",
            )

    try:
        order = service.cancel_order_item(order_id, item_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Order or item not found")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrderService(db)
    existing = service.get_order(order_id)
    if existing is None or existing.restaurant_id != current_user.restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    deleted = service.delete_order(order_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
