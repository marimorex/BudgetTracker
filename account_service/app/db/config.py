import os


class BaseConfig:
    """Base configuration with common settings."""

    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "budget_tracker")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Configuration for development environment."""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Configuration for production environment."""

    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "prod-server")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{BaseConfig.POSTGRES_USER}:{BaseConfig.POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{BaseConfig.POSTGRES_DB}"


class TestingConfig(BaseConfig):
    """Configuration for testing environment."""

    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # In-memory DB for testing
    TESTING = True
