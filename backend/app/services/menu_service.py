from pathlib import Path
from uuid import uuid4

from botocore.exceptions import ClientError
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
        try:
            return self.s3.upload_file(
                file_stream=image.file,
                filename=object_key,
                content_type=content_type,
            )
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code", "Unknown")
            if error_code == "AccessDenied":
                raise ValueError(
                    "Image upload denied by AWS IAM. Grant s3:PutObject on this bucket."
                ) from exc
            if error_code == "NoSuchBucket":
                raise ValueError(
                    "Image upload failed: configured S3 bucket does not exist."
                ) from exc
            raise ValueError(
                f"Image upload failed: AWS error {error_code}.") from exc
        except Exception as exc:
            raise ValueError(
                "Image upload failed. Check AWS S3 bucket settings and credentials."
            ) from exc

    def get_menu_item(self, item_id: int):
        menu_item = self.menu_item_repository.get_by_id(item_id)
        return self._resolve_item_image_url(menu_item)

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
        menu_item = self.menu_item_repository.create(
            name=name,
            price=price,
            is_available=is_available,
            category=category.value,
            image_url=image_url,
        )
        return self._resolve_item_image_url(menu_item)

    def update_menu_item(self, item_id: int, **changes) -> MenuItem:
        menu_item = self.menu_item_repository.get_by_id(item_id)
        if not menu_item:
            raise ValueError(f"Menu item with id {item_id} not found")
        if "category" in changes and isinstance(changes["category"], MenuCategory):
            changes["category"] = changes["category"].value
        updated = self.menu_item_repository.update(menu_item, **changes)
        return self._resolve_item_image_url(updated)

    def delete_menu_item(self, item_id: int) -> None:
        menu_item = self.menu_item_repository.get_by_id(item_id)
        if not menu_item:
            raise ValueError(f"Menu item with id {item_id} not found")
        self.menu_item_repository.delete(menu_item)

    def list_menu_items(self) -> list[MenuItem]:
        items = self.menu_item_repository.list_all()
        return [self._resolve_item_image_url(item) for item in items]

    def _resolve_item_image_url(self, menu_item: MenuItem | None) -> MenuItem | None:
        if menu_item is None or not menu_item.image_url:
            return menu_item

        try:
            menu_item.image_url = self.s3.get_presigned_image_url(
                menu_item.image_url)
        except Exception:
            # Keep original URL if presigning fails.
            pass

        return menu_item
