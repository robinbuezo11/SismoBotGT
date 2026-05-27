from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from urllib.parse import quote_plus

DATABASE_URL = (
    f"mysql+pymysql://{quote_plus(settings.MYSQL_USER)}:"
    f"{quote_plus(settings.MYSQL_PASSWORD)}@"
    f"{settings.MYSQL_HOST}:"
    f"{settings.MYSQL_PORT}/"
    f"{settings.MYSQL_DATABASE}"
    "?charset=utf8mb4"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()