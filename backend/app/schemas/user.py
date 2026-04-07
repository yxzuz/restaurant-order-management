from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    username: str


class OwnerBootstrapCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=72)


class StaffCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=72)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=72)


class UserRead(UserBase):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserDebugRead(UserBase):
    id: int
    role: UserRole
    has_password: bool


class Token(BaseModel):
    access_token: str
    token_type: str
