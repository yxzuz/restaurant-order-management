from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate


class RestaurantRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, restaurant_data: RestaurantCreate) -> Restaurant:
        restaurant = Restaurant(**restaurant_data.model_dump())
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        return self.db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    def get_by_name(self, name: str) -> Restaurant | None:
        return self.db.query(Restaurant).filter(Restaurant.name == name).first()

    def get_all(self) -> list[Restaurant]:
        return self.db.query(Restaurant).all()
