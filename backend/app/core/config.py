import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "INDUSTRIAL INTELLIGENCE"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres_secure_pass@localhost:5432/industrial_intelligence"
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]

    # Scraping Defaults
    DEFAULT_CRAWL_DELAY_SECONDS: float = 2.0
    MAX_RETRIES: int = 3
    USER_AGENT: str = "IndustrialIntelligenceBot/1.0 (+https://example.com/bot; research@industrialintel.local)"
    RESPECT_ROBOTS_TXT: bool = True

    # Storage
    EXPORTS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "exports")

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
