from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from db.config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

# Choose the correct config class
ENV = os.getenv("ENV", "dev")

if ENV == "prod":
    config = ProductionConfig()
elif ENV == "test":
    config = TestingConfig()
else:
    config = DevelopmentConfig()

SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
