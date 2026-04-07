from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User, UserRole
from app.services.auth_service import AuthService, oauth2_bearer


def get_current_user(
    token: str = Depends(oauth2_bearer),
    db: Session = Depends(get_db),
) -> User:
    service = AuthService(db)
    return service.get_current_user(token)


def require_roles(*allowed_roles: UserRole) -> Callable[[User], User]:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            allowed = ", ".join(role.value for role in allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Allowed roles: {allowed}",
            )
        return current_user

    return dependency


require_owner = require_roles(UserRole.OWNER)
require_staff_or_owner = require_roles(UserRole.STAFF, UserRole.OWNER)
