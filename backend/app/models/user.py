from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum, Integer, String
from app.db import Base


class UserRole(str, Enum):
    STAFF = "staff"
    OWNER = "owner"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(
        SQLEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.STAFF,
    )
