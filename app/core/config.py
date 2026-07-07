from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    DATABASE_URL: str

    class Config:
        # Esto le dice a Pydantic que busque el .env dos niveles arriba
        env_file = "../.env"

settings = Settings()
