from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.user import LoginRequest, OwnerBootstrapCreate, StaffCreate
from app.schemas.restaurant import RestaurantCreate

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
        self.restaurant_repository = RestaurantRepository(db)

    def register_owner(self, username: str, password: str, restaurant_name: str) -> tuple[User, str]:
        """Register new restaurant with owner account"""
        # Check if username already exists in any restaurant
        existing_restaurants = self.restaurant_repository.get_all()
        for restaurant in existing_restaurants:
            if self.user_repository.find_existing_user(username, restaurant.id):
                raise ValueError("Username already exists")
        
        # Create restaurant
        restaurant = self.restaurant_repository.create(
            RestaurantCreate(name=restaurant_name)
        )
        
        # Create owner user
        owner = self._create_user(
            username=username,
            password=password,
            restaurant_id=restaurant.id,
            role=UserRole.OWNER,
        )
        
        # Create access token
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = self.create_access_token(
            data={"sub": str(owner.id), "role": owner.role.value, "restaurant_id": restaurant.id},
            expires_delta=expires_delta,
        )
        
        return owner, token

    def bootstrap_owner(self, payload: OwnerBootstrapCreate, restaurant_id: int = 1) -> User:
        """Bootstrap owner for existing restaurant (backward compatibility)"""
        if self.user_repository.owner_exists(restaurant_id):
            raise ValueError("Owner account already exists")

        return self._create_user(
            username=payload.username,
            password=payload.password,
            restaurant_id=restaurant_id,
            role=UserRole.OWNER,
        )

    def create_staff(self, payload: StaffCreate, restaurant_id: int) -> User:
        return self._create_user(
            username=payload.username,
            password=payload.password,
            restaurant_id=restaurant_id,
            role=UserRole.STAFF,
        )

    def delete_staff(self, user_id: int) -> bool:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            return False
        if user.role != UserRole.STAFF:
            raise ValueError("Only staff accounts can be deleted")

        self.user_repository.delete(user)
        return True

    def login(self, payload: LoginRequest) -> str:
        # Try to find user across all restaurants
        all_restaurants = self.restaurant_repository.get_all()
        user = None
        for restaurant in all_restaurants:
            user = self.user_repository.get_by_username(payload.username, restaurant.id)
            if user and bcrypt_context.verify(payload.password, user.hashed_password):
                break
            user = None
        
        if user is None:
            raise ValueError("Invalid username or password")

        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.create_access_token(
            data={"sub": str(user.id), "role": user.role.value, "restaurant_id": user.restaurant_id},
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

    def _create_user(self, *, username: str, password: str, restaurant_id: int, role: UserRole) -> User:
        if self.user_repository.find_existing_user(username, restaurant_id):
            raise ValueError("Username already exists")

        hashed_password = bcrypt_context.hash(password)
        return self.user_repository.create(
            username=username,
            hashed_password=hashed_password,
            restaurant_id=restaurant_id,
            role=role,
        )

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM)
