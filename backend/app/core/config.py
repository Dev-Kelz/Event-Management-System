import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "sqlite:///./event_management.db",
        )
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.ALLOWED_ORIGINS: List[str] = [
            item.strip() for item in os.getenv("ALLOWED_ORIGINS", "*").split(",") if item.strip()
        ]
        self.SESSION_MAX_AGE = int(os.getenv("SESSION_MAX_AGE", "3600"))
        self.DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
        self.DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))


settings = Settings()
