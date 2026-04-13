from fastapi.testclient import TestClient

from .utils import auth_headers, create_staff, login, register_owner


def test_menu_categories_is_public(client: TestClient):
    resp = client.get("/api/menus/categories")
    assert resp.status_code == 200
    categories = resp.json()
    assert isinstance(categories, list)
    assert "Mains" in categories


def test_menu_list_requires_auth(client: TestClient):
    resp = client.get("/api/menus/")
    assert resp.status_code == 401


def test_update_menu_item_requires_fields(client: TestClient):
    token = register_owner(
        client,
        username="owner_menu_update",
        password="pass1234",
        restaurant_name="Menu Update",
    )

    created = client.post(
        "/api/menus/",
        headers=auth_headers(token),
        data={
            "name": "Dish",
            "price": "10.00",
            "category": "Mains",
            "description": "D",
            "is_available": "true",
        },
    )
    assert created.status_code == 201
    item_id = created.json()["id"]

    resp = client.patch(
        f"/api/menus/{item_id}",
        headers=auth_headers(token),
        data={},
    )
    assert resp.status_code == 400


def test_create_menu_item_rejects_non_image_upload(client: TestClient):
    token = register_owner(
        client,
        username="owner_menu_upload",
        password="pass1234",
        restaurant_name="Menu Upload",
    )

    resp = client.post(
        "/api/menus/",
        headers=auth_headers(token),
        data={
            "name": "Dish",
            "price": "10.00",
            "category": "Mains",
            "description": "D",
            "is_available": "true",
        },
        files={
            "image": ("not_image.txt", b"hello", "text/plain"),
        },
    )

    assert resp.status_code == 400


def test_staff_can_update_menu_but_cannot_delete(client: TestClient):
    owner_token = register_owner(
        client,
        username="owner_menu_staff",
        password="pass1234",
        restaurant_name="Menu Staff",
    )

    created = client.post(
        "/api/menus/",
        headers=auth_headers(owner_token),
        data={
            "name": "Dish",
            "price": "10.00",
            "category": "Mains",
            "description": "D",
            "is_available": "true",
        },
    )
    assert created.status_code == 201
    item_id = created.json()["id"]

    create_staff(client, owner_token=owner_token, username="staff_menu", password="pass1234")
    staff_token = login(client, username="staff_menu", password="pass1234")

    update = client.patch(
        f"/api/menus/{item_id}",
        headers=auth_headers(staff_token),
        data={"name": "Updated"},
    )
    assert update.status_code == 200
    assert update.json()["name"] == "Updated"

    delete = client.delete(
        f"/api/menus/{item_id}",
        headers=auth_headers(staff_token),
    )
    assert delete.status_code == 403
