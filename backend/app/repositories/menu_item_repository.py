from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem


class MenuItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, name: str, price, restaurant_id: int, description: str | None = None, is_available: bool = True, category: str = "main course", image_url: str | None = None) -> MenuItem:
        menu_item = MenuItem(
            name=name,
            price=price,
            description=description,
            restaurant_id=restaurant_id,
            is_available=is_available,
            category=category,
            image_url=image_url,
        )
        self.db.add(menu_item)
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    def get_by_id(self, menu_item_id: int) -> MenuItem | None:
        return self.db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()

    def list_all(self, restaurant_id: int) -> list[MenuItem]:
        return self.db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()

    def update(self, menu_item: MenuItem, **changes) -> MenuItem:
        for field, value in changes.items():
            setattr(menu_item, field, value)
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    def delete(self, menu_item: MenuItem) -> None:
        self.db.delete(menu_item)
        self.db.commit()
