from fastapi.testclient import TestClient

from .utils import auth_headers, create_staff, login, register_owner


def _create_menu_item(client: TestClient, token: str, *, name: str = "Dish", description: str = "Desc") -> dict:
    resp = client.post(
        "/api/menus/",
        headers=auth_headers(token),
        data={
            "name": name,
            "price": "99.00",
            "category": "Mains",
            "description": description,
            "is_available": "true",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def _create_table(client: TestClient, token: str, number: int = 1) -> dict:
    resp = client.post(
        "/api/tables/",
        headers=auth_headers(token),
        json={"number": number},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def _create_order(client: TestClient, *, table_number: int, qr_token: str, menu_item_id: int) -> dict:
    resp = client.post(
        "/api/orders/",
        json={
            "table_number": table_number,
            "qr_token": qr_token,
            "items": [{"menu_item_id": menu_item_id, "quantity": 1}],
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_staff_cannot_create_menu_item(client: TestClient):
    owner_token = register_owner(
        client,
        username="owner_role",
        password="pass1234",
        restaurant_name="Role Restaurant",
    )

    create_staff(client, owner_token=owner_token,
                 username="staff_role", password="pass1234")
    staff_token = login(client, username="staff_role", password="pass1234")

    resp = client.post(
        "/api/menus/",
        headers=auth_headers(staff_token),
        data={
            "name": "Staff Dish",
            "price": "10.00",
            "category": "Mains",
            "description": "Should not be allowed",
            "is_available": "true",
        },
    )

    assert resp.status_code == 403


def test_invalid_order_status_transition_rejected(client: TestClient):
    token = register_owner(
        client,
        username="owner_trans",
        password="pass1234",
        restaurant_name="Transitions Restaurant",
    )

    menu_item = _create_menu_item(client, token, name="Dish T")
    table = _create_table(client, token, 1)
    order = _create_order(
        client,
        table_number=1,
        qr_token=table["qr_token"],
        menu_item_id=menu_item["id"],
    )

    # NEW -> COMPLETED is not allowed
    resp = client.patch(
        f"/api/orders/{order['id']}/status",
        headers=auth_headers(token),
        json={"status": "completed"},
    )

    assert resp.status_code == 400


def test_cannot_cancel_items_from_paid_order(client: TestClient):
    token = register_owner(
        client,
        username="owner_paid",
        password="pass1234",
        restaurant_name="Paid Cancel Restaurant",
    )

    menu_item = _create_menu_item(client, token, name="Dish P")
    table = _create_table(client, token, 1)
    order = _create_order(
        client,
        table_number=1,
        qr_token=table["qr_token"],
        menu_item_id=menu_item["id"],
    )

    order_item_id = order["items"][0]["id"]

    # Complete item
    for status in ["PREPARING", "READY", "COMPLETED"]:
        step = client.patch(
            f"/api/orders/{order['id']}/items/{order_item_id}/status",
            headers=auth_headers(token),
            json={"status": status},
        )
        assert step.status_code == 200, step.text

    # Pay
    pay = client.patch(
        f"/api/orders/{order['id']}/payment",
        headers=auth_headers(token),
        json={"payment_status": "paid"},
    )
    assert pay.status_code == 200, pay.text

    # Now cancellation should be blocked
    cancel = client.delete(
        f"/api/orders/{order['id']}/items/{order_item_id}",
        headers=auth_headers(token),
    )
    assert cancel.status_code == 400


def test_cross_tenant_order_and_menu_access_blocked(client: TestClient):
    token_a = register_owner(
        client,
        username="owner_xa",
        password="pass1234",
        restaurant_name="X-A",
    )
    token_b = register_owner(
        client,
        username="owner_xb",
        password="pass1234",
        restaurant_name="X-B",
    )

    menu_item = _create_menu_item(client, token_a, name="Secret Dish")
    table = _create_table(client, token_a, 1)
    order = _create_order(
        client,
        table_number=1,
        qr_token=table["qr_token"],
        menu_item_id=menu_item["id"],
    )

    # Order read is tenant-scoped
    get_order_b = client.get(
        f"/api/orders/{order['id']}",
        headers=auth_headers(token_b),
    )
    assert get_order_b.status_code == 404

    # Menu delete is tenant-scoped
    delete_b = client.delete(
        f"/api/menus/{menu_item['id']}",
        headers=auth_headers(token_b),
    )
    assert delete_b.status_code == 404
