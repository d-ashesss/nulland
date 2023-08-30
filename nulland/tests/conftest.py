import pytest

from fastapi.testclient import TestClient

from nulland.auth import get_public_key
from nulland.db import session
from nulland.main import app
from nulland.tests.utils.auth import jwk_public_key


def override_get_public_key():
    return jwk_public_key.to_dict()


@pytest.fixture(scope="session")
def db():
    return session.SessionLocal()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


session.init_db()
app.dependency_overrides[get_public_key] = override_get_public_key
