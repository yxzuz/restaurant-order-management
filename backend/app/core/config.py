from typing import List
from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    _BASE_DIR = Path(__file__).resolve().parents[2]

    model_config = SettingsConfigDict(
        env_file=_BASE_DIR / ".env",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "Restaurant Order Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "sqlite:///./restaurant.db"
    
    # Security settings
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # AWS S3
    AWS_REGION: str = Field(default="ap-southeast-1", validation_alias=AliasChoices("AWS_REGION", "BUCKET_REGION"))
    AWS_S3_BUCKET: str = Field(validation_alias=AliasChoices("AWS_S3_BUCKET", "BUCKET_NAME"))
    AWS_ACCESS_KEY_ID: SecretStr = Field(validation_alias=AliasChoices("AWS_ACCESS_KEY_ID", "ACCESS_KEY"))
    AWS_SECRET_ACCESS_KEY: SecretStr = Field(validation_alias=AliasChoices("AWS_SECRET_ACCESS_KEY", "SECRET_ACCESS_KEY"))


settings = Settings()
