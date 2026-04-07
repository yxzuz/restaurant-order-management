import secrets

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Restaurant Order Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "sqlite:///./restaurant.db"
    
    # Security settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
