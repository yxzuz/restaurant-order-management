from fastapi.testclient import TestClient

from .utils import auth_headers, register_owner


def test_menu_description_create_update_and_tenant_isolation(client: TestClient):
    token_a = register_owner(
        client,
        username="owner_a",
        password="pass1234",
        restaurant_name="Restaurant A",
    )
    token_b = register_owner(
        client,
        username="owner_b",
        password="pass1234",
        restaurant_name="Restaurant B",
    )

    create_resp = client.post(
        "/api/menus/",
        headers=auth_headers(token_a),
        data={
            "name": "Pad Thai",
            "price": "120.00",
            "category": "Mains",
            "description": "Stir-fried rice noodles with shrimp",
            "is_available": "true",
        },
    )
    assert create_resp.status_code == 201, create_resp.text
    created = create_resp.json()
    assert created["description"] == "Stir-fried rice noodles with shrimp"
    item_id = created["id"]

    # Tenant isolation on list
    list_b = client.get("/api/menus/", headers=auth_headers(token_b))
    assert list_b.status_code == 200
    assert list_b.json() == []

    # Tenant isolation on get
    get_b = client.get(f"/api/menus/{item_id}", headers=auth_headers(token_b))
    assert get_b.status_code == 404

    # Update description (same tenant)
    update_a = client.patch(
        f"/api/menus/{item_id}",
        headers=auth_headers(token_a),
        data={"description": "Classic Thai noodles"},
    )
    assert update_a.status_code == 200, update_a.text
    assert update_a.json()["description"] == "Classic Thai noodles"

    # Cross-tenant update blocked
    update_b = client.patch(
        f"/api/menus/{item_id}",
        headers=auth_headers(token_b),
        data={"description": "Hacked"},
    )
    assert update_b.status_code == 404


def test_qr_menu_endpoint_scopes_to_restaurant(client: TestClient):
    token_a = register_owner(
        client,
        username="owner_a2",
        password="pass1234",
        restaurant_name="Restaurant A2",
    )
    token_b = register_owner(
        client,
        username="owner_b2",
        password="pass1234",
        restaurant_name="Restaurant B2",
    )

    item_a = client.post(
        "/api/menus/",
        headers=auth_headers(token_a),
        data={
            "name": "Green Curry",
            "price": "180.00",
            "category": "Mains",
            "description": "Spicy curry",
            "is_available": "true",
        },
    ).json()

    item_b = client.post(
        "/api/menus/",
        headers=auth_headers(token_b),
        data={
            "name": "Sushi Set",
            "price": "250.00",
            "category": "Mains",
            "description": "Assorted sushi",
            "is_available": "true",
        },
    ).json()

    table_a = client.post(
        "/api/tables/",
        headers=auth_headers(token_a),
        json={"number": 1},
    )
    assert table_a.status_code == 201, table_a.text
    table_a = table_a.json()

    table_b = client.post(
        "/api/tables/",
        headers=auth_headers(token_b),
        json={"number": 1},
    )
    assert table_b.status_code == 201, table_b.text
    table_b = table_b.json()

    # Public QR menu: correct token shows correct restaurant's items.
    menu_a = client.get(f"/api/tables/1/menu?qr_token={table_a['qr_token']}")
    assert menu_a.status_code == 200, menu_a.text
    names_a = {m["name"] for m in menu_a.json()}
    assert item_a["name"] in names_a
    assert item_b["name"] not in names_a

    menu_b = client.get(f"/api/tables/1/menu?qr_token={table_b['qr_token']}")
    assert menu_b.status_code == 200, menu_b.text
    names_b = {m["name"] for m in menu_b.json()}
    assert item_b["name"] in names_b
    assert item_a["name"] not in names_b

    # Invalid token rejected.
    bad = client.get("/api/tables/1/menu?qr_token=not-a-real-token")
    assert bad.status_code == 404
