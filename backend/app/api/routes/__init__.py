from fastapi import APIRouter

from app.api.routes.menus import router as menu_router
from app.api.routes.orders import router as orders_router
from app.api.routes.tables import router as tables_router

router = APIRouter()

router.include_router(orders_router, prefix="/orders", tags=["orders"])
router.include_router(menu_router, prefix="/menus", tags=["menus"])
router.include_router(tables_router, prefix="/tables", tags=["tables"])
