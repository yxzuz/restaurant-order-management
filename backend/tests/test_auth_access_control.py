from fastapi.testclient import TestClient

from .utils import auth_headers, create_staff, login, register_owner


def test_register_owner_token_allows_me_and_includes_restaurant_name(client: TestClient):
    token = register_owner(
        client,
        username="owner_me",
        password="pass1234",
        restaurant_name="Me Restaurant",
    )

    me = client.get("/api/auth/me", headers=auth_headers(token))
    assert me.status_code == 200, me.text
    payload = me.json()

    assert payload["username"] == "owner_me"
    assert payload["role"] == "owner"
    assert isinstance(payload["restaurant_id"], int)
    assert payload["restaurant_name"] == "Me Restaurant"


def test_register_duplicate_username_rejected(client: TestClient):
    register_owner(
        client,
        username="dup_user",
        password="pass1234",
        restaurant_name="First",
    )

    dup = client.post(
        "/api/auth/register",
        json={
            "username": "dup_user",
            "password": "pass1234",
            "restaurant_name": "Second",
        },
    )
    assert dup.status_code == 400


def test_login_invalid_password_rejected(client: TestClient):
    register_owner(
        client,
        username="bad_login",
        password="pass1234",
        restaurant_name="Login R",
    )

    resp = client.post(
        "/api/auth/login",
        json={"username": "bad_login", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_me_requires_auth(client: TestClient):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_owner_can_create_staff_and_staff_role_is_staff(client: TestClient):
    owner_token = register_owner(
        client,
        username="owner_staff_create",
        password="pass1234",
        restaurant_name="Staff Create",
    )

    create_staff(
        client,
        owner_token=owner_token,
        username="staff_created",
        password="pass1234",
    )

    staff_token = login(client, username="staff_created", password="pass1234")
    staff_me = client.get("/api/auth/me", headers=auth_headers(staff_token))
    assert staff_me.status_code == 200
    assert staff_me.json()["role"] == "staff"


def test_staff_cannot_create_staff(client: TestClient):
    owner_token = register_owner(
        client,
        username="owner_staff_lock",
        password="pass1234",
        restaurant_name="Staff Lock",
    )

    create_staff(
        client,
        owner_token=owner_token,
        username="staff_lock",
        password="pass1234",
    )
    staff_token = login(client, username="staff_lock", password="pass1234")

    resp = client.post(
        "/api/auth/staff",
        headers=auth_headers(staff_token),
        json={"username": "other_staff", "password": "pass1234"},
    )
    assert resp.status_code == 403


def test_delete_staff_is_tenant_scoped(client: TestClient):
    owner_a = register_owner(
        client,
        username="owner_del_a",
        password="pass1234",
        restaurant_name="Del A",
    )
    owner_b = register_owner(
        client,
        username="owner_del_b",
        password="pass1234",
        restaurant_name="Del B",
    )

    create_staff(
        client,
        owner_token=owner_b,
        username="staff_del_b",
        password="pass1234",
    )
    staff_token_b = login(client, username="staff_del_b", password="pass1234")
    staff_me_b = client.get(
        "/api/auth/me", headers=auth_headers(staff_token_b))
    staff_id_b = staff_me_b.json()["id"]

    # Owner A should not be able to delete staff from restaurant B
    resp = client.delete(
        f"/api/auth/staff/{staff_id_b}",
        headers=auth_headers(owner_a),
    )
    assert resp.status_code == 404
