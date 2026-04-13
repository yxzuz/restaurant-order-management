from fastapi.testclient import TestClient

from .utils import auth_headers, create_staff, login, register_owner


def _create_menu_item(client: TestClient, token: str, *, name: str, price: str) -> dict:
    resp = client.post(
        "/api/menus/",
        headers=auth_headers(token),
        data={
            "name": name,
            "price": price,
            "category": "Mains",
            "description": "D",
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


def _complete_and_pay_order(client: TestClient, token: str, order: dict) -> dict:
    item_id = order["items"][0]["id"]

    for status in ["PREPARING", "READY", "COMPLETED"]:
        step = client.patch(
            f"/api/orders/{order['id']}/items/{item_id}/status",
            headers=auth_headers(token),
            json={"status": status},
        )
        assert step.status_code == 200, step.text

    pay = client.patch(
        f"/api/orders/{order['id']}/payment",
        headers=auth_headers(token),
        json={"payment_status": "paid"},
    )
    assert pay.status_code == 200, pay.text
    return pay.json()


def test_create_order_invalid_qr_token_forbidden(client: TestClient):
    owner_token = register_owner(
        client,
        username="owner_bad_qr",
        password="pass1234",
        restaurant_name="Bad QR",
    )
    menu_item = _create_menu_item(client, owner_token, name="Dish", price="10.00")

    resp = client.post(
        "/api/orders/",
        json={
            "table_number": 1,
            "qr_token": "not-a-real-token",
            "items": [{"menu_item_id": menu_item["id"], "quantity": 1}],
        },
    )
    assert resp.status_code == 403


def test_create_order_rejects_cross_restaurant_menu_item(client: TestClient):
    token_a = register_owner(
        client,
        username="owner_order_a",
        password="pass1234",
        restaurant_name="Order A",
    )
    token_b = register_owner(
        client,
        username="owner_order_b",
        password="pass1234",
        restaurant_name="Order B",
    )

    item_b = _create_menu_item(client, token_b, name="Other Dish", price="10.00")
    table_a = _create_table(client, token_a, 1)

    resp = client.post(
        "/api/orders/",
        json={
            "table_number": 1,
            "qr_token": table_a["qr_token"],
            "items": [{"menu_item_id": item_b["id"], "quantity": 1}],
        },
    )
    assert resp.status_code == 403


def test_customer_cancel_requires_valid_qr_token(client: TestClient):
    token = register_owner(
        client,
        username="owner_cancel_qr",
        password="pass1234",
        restaurant_name="Cancel QR",
    )

    menu_item = _create_menu_item(client, token, name="Dish", price="10.00")
    table = _create_table(client, token, 1)
    order = _create_order(
        client,
        table_number=1,
        qr_token=table["qr_token"],
        menu_item_id=menu_item["id"],
    )
    order_item_id = order["items"][0]["id"]

    no_qr = client.delete(f"/api/orders/{order['id']}/items/{order_item_id}")
    assert no_qr.status_code == 403

    wrong_qr = client.delete(
        f"/api/orders/{order['id']}/items/{order_item_id}?qr_token=wrong"
    )
    assert wrong_qr.status_code == 403

    ok = client.delete(
        f"/api/orders/{order['id']}/items/{order_item_id}?qr_token={table['qr_token']}"
    )
    assert ok.status_code == 200, ok.text


def test_reports_require_owner_and_are_tenant_scoped(client: TestClient):
    token_a = register_owner(
        client,
        username="owner_rep_a",
        password="pass1234",
        restaurant_name="Rep A",
    )
    token_b = register_owner(
        client,
        username="owner_rep_b",
        password="pass1234",
        restaurant_name="Rep B",
    )

    # No auth -> 401
    no_auth = client.get("/api/reports/analytics")
    assert no_auth.status_code == 401

    # Create paid order in restaurant A (100.00)
    item_a = _create_menu_item(client, token_a, name="A Dish", price="100.00")
    table_a = _create_table(client, token_a, 1)
    order_a = _create_order(
        client,
        table_number=1,
        qr_token=table_a["qr_token"],
        menu_item_id=item_a["id"],
    )
    paid_a = _complete_and_pay_order(client, token_a, order_a)

    # Create paid order in restaurant B (200.00)
    item_b = _create_menu_item(client, token_b, name="B Dish", price="200.00")
    table_b = _create_table(client, token_b, 1)
    order_b = _create_order(
        client,
        table_number=1,
        qr_token=table_b["qr_token"],
        menu_item_id=item_b["id"],
    )
    paid_b = _complete_and_pay_order(client, token_b, order_b)

    assert paid_a["payment_status"].lower() == "paid"
    assert paid_b["payment_status"].lower() == "paid"

    analytics_a = client.get("/api/reports/analytics", headers=auth_headers(token_a))
    assert analytics_a.status_code == 200, analytics_a.text
    total_revenue_a = analytics_a.json()["overall_stats"]["total_revenue"]
    assert total_revenue_a == 100.0

    analytics_b = client.get("/api/reports/analytics", headers=auth_headers(token_b))
    assert analytics_b.status_code == 200, analytics_b.text
    total_revenue_b = analytics_b.json()["overall_stats"]["total_revenue"]
    assert total_revenue_b == 200.0


def test_staff_forbidden_from_reports(client: TestClient):
    owner_token = register_owner(
        client,
        username="owner_rep_staff",
        password="pass1234",
        restaurant_name="Rep Staff",
    )

    create_staff(client, owner_token=owner_token, username="staff_rep", password="pass1234")
    staff_token = login(client, username="staff_rep", password="pass1234")

    resp = client.get("/api/reports/daily-sales", headers=auth_headers(staff_token))
    assert resp.status_code == 403
