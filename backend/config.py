# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings with validation"""
    
    def __init__(self):
        # Required settings
        self.SECRET_KEY = self._get_required_env("SECRET_KEY")
        self.DATABASE_URL = self._get_required_env("DATABASE_URL")
        
        # Optional settings with defaults
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
        
        # Session settings
        self.SESSION_MAX_AGE = int(os.getenv("SESSION_MAX_AGE", "3600"))  # 1 hour default
        
        # Database settings
        self.DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
        self.DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
        
        # Security settings
        self.RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        self.LOGIN_RATE_LIMIT = os.getenv("LOGIN_RATE_LIMIT", "5/minute")
        
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable or raise error"""
        value = os.getenv(key)
        if not value:
            raise ValueError(
                f"Required environment variable '{key}' is not set. "
                f"Please set it in your .env file or environment."
            )
        return value
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"


# Create global settings instance
settings = Settings()

