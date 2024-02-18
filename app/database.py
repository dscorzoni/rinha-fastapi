from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database Configuration
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres@db/postgres"  # For Docker
# For Local Development
SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost/postgres"
db_engine = create_engine(SQLALCHEMY_DATABASE_URL,
                          pool_size=20, max_overflow=0)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine
    )
)
Model = declarative_base()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
