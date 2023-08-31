from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ._base import Base
from nulland.config import settings


engine = create_engine(str(settings.database_uri))
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def init_db():
    """Applies all migrations to initialize new database."""
    Base.metadata.create_all(engine)


def get_db():
    """Creates a new session for each request."""
    with SessionLocal() as db:
        yield db
