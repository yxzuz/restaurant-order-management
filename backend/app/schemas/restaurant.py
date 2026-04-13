from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RestaurantBase(BaseModel):
    name: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantRead(RestaurantBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
