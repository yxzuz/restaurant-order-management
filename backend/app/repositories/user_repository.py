from sqlalchemy.orm import Session

from app.models.user import User, UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, username: str, hashed_password: str, restaurant_id: int, role: UserRole = UserRole.STAFF) -> User:
        user = User(username=username, hashed_password=hashed_password,
                    restaurant_id=restaurant_id, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str, restaurant_id: int) -> User | None:
        return self.db.query(User).filter(
            User.username == username,
            User.restaurant_id == restaurant_id
        ).first()

    def get_first_owner(self, restaurant_id: int) -> User | None:
        return self.db.query(User).filter(
            User.role == UserRole.OWNER,
            User.restaurant_id == restaurant_id
        ).first()

    def owner_exists(self, restaurant_id: int) -> bool:
        return self.get_first_owner(restaurant_id) is not None

    def list_all(self, restaurant_id: int) -> list[User]:
        return self.db.query(User).filter(User.restaurant_id == restaurant_id).all()

    def update(self, user: User, **changes) -> User:
        for field, value in changes.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

    def find_existing_user(self, username: str, restaurant_id: int) -> User | None:
        return self.db.query(User).filter(
            User.username == username,
            User.restaurant_id == restaurant_id
        ).first()
