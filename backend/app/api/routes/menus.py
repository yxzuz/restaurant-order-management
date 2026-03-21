from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.menu_item import MenuItemCreate, MenuItemRead, MenuItemUpdate
from app.services.menu_service import MenuService

router = APIRouter()


@router.get("/", response_model=list[MenuItemRead])
def list_menus(db: Session = Depends(get_db)):
    service = MenuService(db)
    # return service.list_menu_items()
    return service.mock_get_menu()


@router.get("/{item_id}", response_model=MenuItemRead)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    service = MenuService(db)
    menu_item = service.get_menu_item(item_id)
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return menu_item


@router.post("/", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
def create_menu_item(payload: MenuItemCreate, db: Session = Depends(get_db)):
    service = MenuService(db)
    return service.create_menu_item(
        name=payload.name,
        price=payload.price,
        is_available=payload.is_available,
    )


@router.patch("/{item_id}", response_model=MenuItemRead)
def update_menu_item(item_id: int, payload: MenuItemUpdate, db: Session = Depends(get_db)):
    service = MenuService(db)
    try:
        return service.update_menu_item(item_id, **payload.model_dump(exclude_unset=True))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    service = MenuService(db)
    try:
        service.delete_menu_item(item_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
