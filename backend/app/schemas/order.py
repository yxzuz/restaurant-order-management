from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.order import OrderStatus, PaymentStatus
from app.schemas.order_item import OrderItemCreate, OrderItemRead
from app.schemas.table import TableRead


class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.NEW


class OrderCreate(BaseModel):
    table_number: int
    qr_token: str
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderPaymentUpdate(BaseModel):
    payment_status: PaymentStatus


class OrderRead(OrderBase):
    id: int
    table_id: int
    payment_status: PaymentStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None
    closed_at: datetime | None = None
    table: TableRead | None = None
    items: list[OrderItemRead] = []

    model_config = ConfigDict(from_attributes=True)
