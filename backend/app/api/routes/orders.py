from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.order import OrderCreate, OrderPaymentUpdate, OrderRead, OrderUpdate
from app.services.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=list[OrderRead])
def list_orders(db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.list_orders()


@router.get("/active", response_model=list[OrderRead])
def list_active_orders(db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.list_active_orders()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    service = OrderService(db)
    try:
        return service.create_order(payload.model_dump())
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(order_id: int, payload: OrderUpdate, db: Session = Depends(get_db)):
    if payload.status is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status is required",
        )

    service = OrderService(db)
    try:
        order = service.update_order_status(order_id, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{order_id}/payment", response_model=OrderRead)
def update_order_payment(order_id: int, payload: OrderPaymentUpdate, db: Session = Depends(get_db)):
    service = OrderService(db)
    try:
        order = service.update_payment_status(order_id, payload.payment_status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    service = OrderService(db)
    deleted = service.delete_order(order_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
