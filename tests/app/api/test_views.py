import json

from flask import Response

from app.db_function import create_products_type_from_propulate_db, create_user_test


def test_login(client, app):
    # Create user test
    with app.app_context():
        create_user_test()

    # Send request
    headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Basic bWFpc3RvZG9zOm1haXN0b2Rvcw==",
    }
    response: Response = client.post("/api/login", headers=headers)
    assert response.status_code == 200


def test_cashbak(client, mocker, app):
    # Populate db
    with app.app_context():
        create_user_test()
        create_products_type_from_propulate_db()

    # Get token
    get_token_headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Basic bWFpc3RvZG9zOm1haXN0b2Rvcw==",
    }
    token: str = (
        client.post("/api/login", headers=get_token_headers).get_json().get("token")
    )

    # Send request
    headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }
    data: dict = {
        "sold_at": "2023-01-02 00:00:00",
        "customer": {"document": "681.755.410-16", "name": "JOSE DA SILVA"},
        "total": "100.00",
        "products": [
            {"type": "A", "value": "10.00", "qty": 1},
            {"type": "B", "value": "10.00", "qty": 9},
        ],
    }
    mocker.patch(
        "app.api.views.send_cashback",
        return_value={
            "createdAt": "2022-12-22T15:33:05.244Z",
            "message": "Cashback criado com sucesso!",
            "id": "1",
            "document": "33535353535",
            "cashback": "10",
        },
    )
    response: Response = client.post(
        "/api/cashback", headers=headers, data=json.dumps(data)
    )
    assert response.get_json() == {"message": "success"}
    assert response.status_code == 200
