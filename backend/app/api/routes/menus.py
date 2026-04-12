from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_owner, require_staff_or_owner
from app.db import get_db
from app.schemas.menu_item import MenuCategory, MenuItemRead
from app.services.menu_service import MenuService

router = APIRouter()


@router.get("/", response_model=list[MenuItemRead])
def list_menus(db: Session = Depends(get_db)):
    service = MenuService(db)
    return service.list_menu_items()


@router.get("/categories", response_model=list[MenuCategory])
def list_menu_categories():
    return MenuService.list_categories()


@router.get("/{item_id}", response_model=MenuItemRead)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    service = MenuService(db)
    menu_item = service.get_menu_item(item_id)
    if menu_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return menu_item

# crud operations for menu items, only accessible by the owner of the restaurant


@router.post("/", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
def create_menu_item(
    name: str = Form(...),
    price: Decimal = Form(...),
    category: MenuCategory = Form(...),
    is_available: bool = Form(True),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    _current_user=Depends(require_owner),
):
    service = MenuService(db)
    image_url = None
    if image is not None:
        try:
            image_url = service.upload_menu_image(image)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return service.create_menu_item(
        name=name,
        price=price,
        is_available=is_available,
        category=category,
        image_url=image_url,
    )


@router.patch("/{item_id}", response_model=MenuItemRead)
@router.put("/{item_id}", response_model=MenuItemRead)
def update_menu_item(
    item_id: int,
    name: str | None = Form(None),
    price: Decimal | None = Form(None),
    category: MenuCategory | None = Form(None),
    is_available: bool | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    _current_user=Depends(require_staff_or_owner),
):
    service = MenuService(db)
    changes = {}
    if name is not None:
        changes["name"] = name
    if price is not None:
        changes["price"] = price
    if category is not None:
        changes["category"] = category
    if is_available is not None:
        changes["is_available"] = is_available
    if image is not None:
        try:
            changes["image_url"] = service.upload_menu_image(image)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not changes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No fields provided for update")

    try:
        return service.update_menu_item(item_id, **changes)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: int, db: Session = Depends(get_db), _current_user=Depends(require_owner)):
    service = MenuService(db)
    try:
        service.delete_menu_item(item_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
