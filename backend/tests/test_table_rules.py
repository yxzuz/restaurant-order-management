from fastapi.testclient import TestClient

from .utils import auth_headers, create_staff, login, register_owner


def test_owner_can_create_and_list_tables(client: TestClient):
    token = register_owner(
        client,
        username="owner_table_list",
        password="pass1234",
        restaurant_name="Tables",
    )

    created = client.post(
        "/api/tables/",
        headers=auth_headers(token),
        json={"number": 1},
    )
    assert created.status_code == 201, created.text

    tables = client.get("/api/tables/", headers=auth_headers(token))
    assert tables.status_code == 200
    assert any(t["number"] == 1 for t in tables.json())


def test_staff_can_list_tables(client: TestClient):
    owner_token = register_owner(
        client,
        username="owner_table_staff",
        password="pass1234",
        restaurant_name="Tables Staff",
    )

    client.post(
        "/api/tables/",
        headers=auth_headers(owner_token),
        json={"number": 1},
    )

    create_staff(client, owner_token=owner_token, username="staff_tables", password="pass1234")
    staff_token = login(client, username="staff_tables", password="pass1234")

    resp = client.get("/api/tables/", headers=auth_headers(staff_token))
    assert resp.status_code == 200
    assert any(t["number"] == 1 for t in resp.json())


def test_table_access_links_owner_only(client: TestClient):
    owner_token = register_owner(
        client,
        username="owner_links",
        password="pass1234",
        restaurant_name="Links",
    )

    create_staff(client, owner_token=owner_token, username="staff_links", password="pass1234")
    staff_token = login(client, username="staff_links", password="pass1234")

    resp = client.get("/api/tables/access-links", headers=auth_headers(staff_token))
    assert resp.status_code == 403


def test_duplicate_table_number_same_restaurant_rejected(client: TestClient):
    token = register_owner(
        client,
        username="owner_dup_table",
        password="pass1234",
        restaurant_name="Dup Table",
    )

    first = client.post(
        "/api/tables/",
        headers=auth_headers(token),
        json={"number": 1},
    )
    assert first.status_code == 201

    second = client.post(
        "/api/tables/",
        headers=auth_headers(token),
        json={"number": 1},
    )
    assert second.status_code == 400


def test_same_table_number_different_restaurants_allowed(client: TestClient):
    token_a = register_owner(
        client,
        username="owner_ta",
        password="pass1234",
        restaurant_name="Tenant A",
    )
    token_b = register_owner(
        client,
        username="owner_tb",
        password="pass1234",
        restaurant_name="Tenant B",
    )

    a = client.post(
        "/api/tables/",
        headers=auth_headers(token_a),
        json={"number": 1},
    )
    assert a.status_code == 201

    b = client.post(
        "/api/tables/",
        headers=auth_headers(token_b),
        json={"number": 1},
    )
    assert b.status_code == 201


def test_delete_table_with_order_history_rejected(client: TestClient):
    token = register_owner(
        client,
        username="owner_delete_hist",
        password="pass1234",
        restaurant_name="Del Hist",
    )

    menu_item = client.post(
        "/api/menus/",
        headers=auth_headers(token),
        data={
            "name": "Dish",
            "price": "10.00",
            "category": "Mains",
            "description": "D",
            "is_available": "true",
        },
    ).json()

    table = client.post(
        "/api/tables/",
        headers=auth_headers(token),
        json={"number": 1},
    ).json()

    order = client.post(
        "/api/orders/",
        json={
            "table_number": 1,
            "qr_token": table["qr_token"],
            "items": [{"menu_item_id": menu_item["id"], "quantity": 1}],
        },
    )
    assert order.status_code == 201

    resp = client.delete("/api/tables/1", headers=auth_headers(token))
    assert resp.status_code == 400
