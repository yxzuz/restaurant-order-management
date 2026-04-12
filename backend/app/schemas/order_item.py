from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.menu_item import MenuItemRead


class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int = Field(default=1, ge=1)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: int | None = Field(default=None, ge=1)


class OrderItemStatusUpdate(BaseModel):
    status: str


class OrderItemRead(BaseModel):
    id: int
    order_id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal
    status: str = "NEW"
    created_at: datetime | None = None
    updated_at: datetime | None = None
    menu_item: MenuItemRead | None = None

    model_config = ConfigDict(from_attributes=True)
