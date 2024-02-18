from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Database Configuration
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres@db/postgres"
# For Local Development
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres@localhost/postgres"

db_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=30,
    max_overflow=0,
    isolation_level="READ COMMITTED"
)

db_session = async_sessionmaker(
    bind=db_engine,
    autoflush=False,
    future=True
)

Model = declarative_base()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
