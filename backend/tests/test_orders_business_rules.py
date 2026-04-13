from fastapi.testclient import TestClient

from .utils import auth_headers, register_owner


def _create_menu_item(client: TestClient, token: str) -> dict:
    resp = client.post(
        "/api/menus/",
        headers=auth_headers(token),
        data={
            "name": "Tom Yum",
            "price": "150.00",
            "category": "Mains",
            "description": "Soup",
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


def test_payment_requires_completed_items_and_frees_table(client: TestClient):
    token = register_owner(
        client,
        username="owner_pay",
        password="pass1234",
        restaurant_name="Pay Rules Restaurant",
    )

    menu_item = _create_menu_item(client, token)
    table = _create_table(client, token, 1)

    # Customer creates an order (public endpoint, validated by QR token)
    order_resp = client.post(
        "/api/orders/",
        json={
            "table_number": 1,
            "qr_token": table["qr_token"],
            "items": [{"menu_item_id": menu_item["id"], "quantity": 1}],
        },
    )
    assert order_resp.status_code == 201, order_resp.text
    order = order_resp.json()
    assert order["payment_status"].lower() == "unpaid"
    assert len(order["items"]) == 1
    order_item_id = order["items"][0]["id"]

    # Cannot mark paid without auth
    no_auth_pay = client.patch(
        f"/api/orders/{order['id']}/payment",
        json={"payment_status": "paid"},
    )
    assert no_auth_pay.status_code == 401

    # Cannot mark paid until all items are completed
    pay_fail = client.patch(
        f"/api/orders/{order['id']}/payment",
        headers=auth_headers(token),
        json={"payment_status": "paid"},
    )
    assert pay_fail.status_code == 400

    # Advance item through the allowed lifecycle (ItemStatus values are uppercase)
    for status in ["PREPARING", "READY", "COMPLETED"]:
        step = client.patch(
            f"/api/orders/{order['id']}/items/{order_item_id}/status",
            headers=auth_headers(token),
            json={"status": status},
        )
        assert step.status_code == 200, step.text

    pay_ok = client.patch(
        f"/api/orders/{order['id']}/payment",
        headers=auth_headers(token),
        json={"payment_status": "paid"},
    )
    assert pay_ok.status_code == 200, pay_ok.text
    paid_order = pay_ok.json()
    assert paid_order["payment_status"].lower() == "paid"

    # Table should be freed once paid
    tables = client.get("/api/tables/", headers=auth_headers(token))
    assert tables.status_code == 200
    table_1 = next(t for t in tables.json() if t["number"] == 1)
    assert table_1["status"] == "available"
