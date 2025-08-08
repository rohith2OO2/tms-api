import os
from functools import lru_cache


class Settings:
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite+aiosqlite:///./tms.db"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "changeme")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@example.com")


class Config:
    env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
