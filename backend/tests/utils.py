from fastapi.testclient import TestClient


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register_owner(client: TestClient, *, username: str, password: str, restaurant_name: str) -> str:
    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": password,
            "restaurant_name": restaurant_name,
        },
    )
    assert response.status_code == 201, response.text
    payload = response.json()
    assert "access_token" in payload
    return payload["access_token"]


def login(client: TestClient, *, username: str, password: str) -> str:
    response = client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert "access_token" in payload
    return payload["access_token"]


def create_staff(client: TestClient, *, owner_token: str, username: str, password: str) -> dict:
    response = client.post(
        "/api/auth/staff",
        headers=auth_headers(owner_token),
        json={
            "username": username,
            "password": password,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()
