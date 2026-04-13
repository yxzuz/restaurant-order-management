from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user, require_owner
from app.db import get_db
from app.models.user import User
from app.schemas.user import (
    LoginRequest,
    MessageResponse,
    OwnerBootstrapCreate,
    RegistrationRequest,
    StaffCreate,
    Token,
    UserDebugRead,
    UserRead,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: RegistrationRequest, db: Session = Depends(get_db)):
    """Register a new restaurant with owner account"""
    service = AuthService(db)
    try:
        owner, token = service.register_owner(
            username=payload.username,
            password=payload.password,
            restaurant_name=payload.restaurant_name
        )
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/bootstrap-owner", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def bootstrap_owner(payload: OwnerBootstrapCreate, db: Session = Depends(get_db)):
    # This endpoint allows creating the initial owner account. It should only be used once during setup.
    service = AuthService(db)
    try:
        return service.bootstrap_owner(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        access_token = service.login(payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    # Manually construct response to include restaurant name
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "restaurant_id": current_user.restaurant_id,
        "restaurant_name": current_user.restaurant.name if current_user.restaurant else None,
    }


@router.post("/logout", response_model=MessageResponse)
def logout(current_user: User = Depends(get_current_user)):
    return {"message": f"User '{current_user.username}' logged out successfully"}


@router.post("/staff", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_staff(
    payload: StaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    service = AuthService(db)
    try:
        return service.create_staff(payload, current_user.restaurant_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/debug/users", response_model=list[UserDebugRead])
def debug_list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    service = AuthService(db)
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "has_password": bool(user.hashed_password),
        }
        for user in service.user_repository.list_all(current_user.restaurant_id)
    ]


@router.delete("/staff/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    service = AuthService(db)
    try:
        deleted = service.delete_staff(user_id, current_user.restaurant_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Staff account not found")
