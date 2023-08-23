from fastapi.testclient import TestClient


def auth_headers(private_key) -> dict[str, str]:
    from jose import jwt
    claims = {"sub": "test-user-1", "name": "John Doe", "email": "joe@localhost"}
    token = jwt.encode(claims, private_key, algorithm="RS256")
    return {"Authorization": f"Bearer {token}"}


def test_list_notes(client: TestClient, private_key):
    response = client.get("/notes", headers=auth_headers(private_key))
    assert response.status_code == 200
    assert response.text == "[]"
