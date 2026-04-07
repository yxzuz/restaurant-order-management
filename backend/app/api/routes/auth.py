from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_owner
from app.db import get_db
from app.schemas.user import (
    LoginRequest,
    OwnerBootstrapCreate,
    StaffCreate,
    Token,
    UserDebugRead,
    UserRead,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/bootstrap-owner", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def bootstrap_owner(payload: OwnerBootstrapCreate, db: Session = Depends(get_db)):
    # This endpoint allows creating the initial owner account. It should only be used once during setup.
    service = AuthService(db)
    try:
        return service.bootstrap_owner(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        access_token = service.login(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/staff", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_staff(
    payload: StaffCreate,
    db: Session = Depends(get_db),
    _current_user = Depends(require_owner),
):
    service = AuthService(db)
    try:
        return service.create_staff(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/debug/users", response_model=list[UserDebugRead])
def debug_list_users(
    db: Session = Depends(get_db),
    _current_user = Depends(require_owner),
):
    service = AuthService(db)
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "has_password": bool(user.hashed_password),
        }
        for user in service.user_repository.list_all()
    ]
