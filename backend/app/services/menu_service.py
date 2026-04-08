from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.repositories.menu_item_repository import MenuItemRepository
from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuCategory
from app.services.s3_service import s3_service


class MenuService:
    def __init__(self, db_session, s3_client_service=s3_service):
        self.db_session = db_session
        self.menu_item_repository = MenuItemRepository(db_session)
        self.s3 = s3_client_service

    def upload_menu_image(self, image: UploadFile) -> str:
        content_type = image.content_type or ""
        if not content_type.startswith("image/"):
            raise ValueError("Only image files are allowed")

        extension = Path(image.filename or "").suffix or ".jpg"
        object_key = f"menu-items/{uuid4().hex}{extension}"
        return self.s3.upload_file(
            file_stream=image.file,
            filename=object_key,
            content_type=content_type,
        )

    def get_menu_item(self, item_id: int):
        return self.menu_item_repository.get_by_id(item_id)
    
    @staticmethod
    def list_categories() -> list[MenuCategory]:
        return list(MenuCategory)

    def create_menu_item(
        self,
        name: str,
        price: float,
        is_available: bool = True,
        category: MenuCategory = MenuCategory.MAIN_COURSE,
        image_url: str | None = None,
    ) -> MenuItem:
        return self.menu_item_repository.create(
            name=name,
            price=price,
            is_available=is_available,
            category=category.value,
            image_url=image_url,
        )
    
    
    def update_menu_item(self, item_id: int, **changes) -> MenuItem:
        menu_item = self.menu_item_repository.get_by_id(item_id)
        if not menu_item:
            raise ValueError(f"Menu item with id {item_id} not found")
        if "category" in changes and isinstance(changes["category"], MenuCategory):
            changes["category"] = changes["category"].value
        return self.menu_item_repository.update(menu_item, **changes)
    
    def delete_menu_item(self, item_id: int) -> None:
        menu_item = self.menu_item_repository.get_by_id(item_id)
        if not menu_item:
            raise ValueError(f"Menu item with id {item_id} not found")
        self.menu_item_repository.delete(menu_item)
        
    def list_menu_items(self) -> list[MenuItem]:
        return self.menu_item_repository.list_all()
