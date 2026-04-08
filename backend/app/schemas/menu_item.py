from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict


class MenuCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main course"
    DESSERT = "dessert"
    DRINK = "drink"


class MenuItemBase(BaseModel):
    name: str
    price: Decimal
    is_available: bool = True
    category: MenuCategory


class MenuItemCreate(MenuItemBase):
    image_url: str | None = None


class MenuItemUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    is_available: bool | None = None
    category: MenuCategory | None = None
    image_url: str | None = None


class MenuItemRead(MenuItemBase):
    id: int
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
