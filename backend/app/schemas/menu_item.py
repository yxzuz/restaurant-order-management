from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class MenuItemBase(BaseModel):
    name: str
    price: Decimal
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    is_available: bool | None = None


class MenuItemRead(MenuItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
