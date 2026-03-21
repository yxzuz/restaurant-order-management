from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.order import OrderStatus
from app.schemas.order_item import OrderItemCreate, OrderItemRead


class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.NEW


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderRead(OrderBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    items: list[OrderItemRead] = []

    model_config = ConfigDict(from_attributes=True)
