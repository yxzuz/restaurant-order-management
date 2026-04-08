from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.user import LoginRequest, OwnerBootstrapCreate, StaffCreate

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def bootstrap_owner(self, payload: OwnerBootstrapCreate) -> User:
        if self.user_repository.owner_exists():
            raise ValueError("Owner account already exists")

        return self._create_user(
            username=payload.username,
            password=payload.password,
            role=UserRole.OWNER,
        )

    def create_staff(self, payload: StaffCreate) -> User:
        return self._create_user(
            username=payload.username,
            password=payload.password,
            role=UserRole.STAFF,
        )

    def login(self, payload: LoginRequest) -> str:
        user = self.user_repository.get_by_username(payload.username)
        if user is None or not bcrypt_context.verify(payload.password, user.hashed_password):
            raise ValueError("Invalid username or password")

        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.create_access_token(
            data={"sub": str(user.id), "role": user.role.value},
            expires_delta=expires_delta,
        )

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError as exc:
            raise credentials_exception from exc

        user = self.user_repository.get_by_id(int(user_id))
        if user is None:
            raise credentials_exception
        return user

    def require_owner(self, token: str) -> User:
        user = self.get_current_user(token)
        if user.role != UserRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Owner access required",
            )
        return user

    def _create_user(self, *, username: str, password: str, role: UserRole) -> User:
        if self.user_repository.find_existing_user(username):
            raise ValueError("Username already exists")

        hashed_password = bcrypt_context.hash(password)
        return self.user_repository.create(
            username=username,
            hashed_password=hashed_password,
            role=role,
        )

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM)
