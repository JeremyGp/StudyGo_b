from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "StudyGo"
    DATABASE_URL: str = "sqlite:///./studygo.db"
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if isinstance(value, str):
            cleaned_value = value.strip()
            if not cleaned_value or "{usuario}" in cleaned_value or "{contraseña}" in cleaned_value:
                return "sqlite:///./studygo.db"
            return cleaned_value
        return value

settings = Settings()