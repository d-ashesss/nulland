import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base


engine = create_engine(os.getenv("DATABASE_URI"))
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def get_db():
    with SessionLocal() as db:
        yield db
