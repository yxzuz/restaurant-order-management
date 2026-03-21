from app.repositories.menu_item_repository import MenuItemRepository
from backend.app.models.menu_item import MenuItem

class MenuService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.menu_item_repository = MenuItemRepository(db_session)

    def mock_get_menu(self):
        # This is a placeholder implementation. In a real application, you would query the database.
        return [
            {"id": 1, "name": "Margherita Pizza", "price": 8.99},
            {"id": 2, "name": "Pepperoni Pizza", "price": 9.99},
            {"id": 3, "name": "Veggie Pizza", "price": 10.99},
        ]
    
    def get_menu_item(self, item_id: int):
        return self.menu_item_repository.get_by_id(item_id)
    
    def create_menu_item(self, name: str, price: float, is_available: bool = True) -> MenuItem:
        return self.menu_item_repository.create(name=name, price=price, is_available=is_available)
    
    def update_menu_item(self, item_id: int, **changes) -> MenuItem:
        menu_item = self.menu_item_repository.get_by_id(item_id)
        if not menu_item:
            raise ValueError(f"Menu item with id {item_id} not found")
        return self.menu_item_repository.update(menu_item, **changes)
    
    def delete_menu_item(self, item_id: int) -> None:
        menu_item = self.menu_item_repository.get_by_id(item_id)
        if not menu_item:
            raise ValueError(f"Menu item with id {item_id} not found")
        self.menu_item_repository.delete(menu_item)
        
    def list_menu_items(self) -> list[MenuItem]:
        return self.menu_item_repository.list_all()
    
            