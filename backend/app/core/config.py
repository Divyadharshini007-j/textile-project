import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Yarn Trading Accountancy"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./yarn_trading.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt-token-generation")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
