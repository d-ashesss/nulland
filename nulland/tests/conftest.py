import pytest

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient
from jose import jwk

rsa_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
private_key = rsa_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
jwk_private_key = jwk.RSAKey(key=private_key.decode('utf-8'), algorithm='RS256')
public_key = rsa_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
jwk_public_key = jwk.RSAKey(key=public_key.decode('utf-8'), algorithm='RS256')


from nulland.auth import get_public_key
from nulland.main import app


def override_get_public_key():
    return jwk_public_key.to_dict()

app.dependency_overrides[get_public_key] = override_get_public_key


@pytest.fixture
def private_key():
    return jwk_private_key


from nulland.db import session
session.init_db()


@pytest.fixture(scope="session")
def db():
    return session.SessionLocal()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
