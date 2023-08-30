from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
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


def auth_headers(user_id) -> dict[str, str]:
    from jose import jwt
    claims = {"sub": str(user_id), "name": "John Doe", "email": "joe@localhost"}
    token = jwt.encode(claims, jwk_private_key, algorithm="RS256")
    return {"Authorization": f"Bearer {token}"}
