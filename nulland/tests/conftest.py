import pytest

from fastapi.testclient import TestClient

from nulland.db import session
from nulland.main import app


@pytest.fixture(scope="session")
def db():
    return session.SessionLocal()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


session.init_db()
