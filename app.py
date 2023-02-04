from typing import Optional

from flask import Flask, jsonify, request
from marshmallow.exceptions import ValidationError
from requests import Response, post

from db_function import get_products_by_types
from models import LogApi, ProductType
from schema import CashbackSchema, configure_app

app = Flask(__name__)
configure_app(app)


def cashback_calculate(products_data: list[dict]) -> float:
    products_type: list[ProductType] = get_products_by_types(products_data)

    cashback: float = 0.0
    for product_data in products_data:
        for product_type in products_type:
            if product_data.get("type") == product_type.name:
                cashback: float = cashback + (
                    (product_data.get("value") * product_data.get("qty"))
                    * product_type.cashback_percentage
                    / 100
                )
    return cashback


def send_cashback(cashback_value: float, document: str) -> dict:
    payload = {"document": document, "cashback": cashback_value}
    url = "https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback"
    headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
    }
    try:
        response: Optional[Response] = post(url=url, json=payload, headers=headers)
    except Exception:
        # TODO Save the error when creating the log saving mechanism
        response: Optional[Response] = None

    response_data: dict = {}
    if response is not None:
        if response.status_code == 200:
            response_data: dict = response.json()
        else:
            response_data["error_message"] = str(response.text).replace('"', "")

        # Save log API
        LogApi.save_log(
            _request=response.request,
            response_json=response_data,
            app="MaisTodosAPI",
            status_code=response.status_code,
        )
    else:
        response_data["error_message"] = "Error sending cashback to MaisTodos API"

    # response_data = {
    #     "createdAt": "2022-12-22T15:33:05.244Z",
    #     "message": "Cashback criado com sucesso!",
    #     "id": "1",
    #     "document": "33535353535",
    #     "cashback": "10",
    # }
    return response_data


@app.route("/api/cashback", methods=["POST"])
def cashback():
    data: dict = request.get_json()
    try:
        schema: Optional[dict] = CashbackSchema().load(data)
        if schema is None:
            response_json = {
                "error_message": "It was not possible to validate the sent data, invalid data"
            }
            # Save log API
            LogApi.save_log(
                _request=request,
                response_json=response_json,
                app="localhost-cashback",
                status_code=400,
            )
            return jsonify(response_json), 400
    except ValidationError as error:
        response_json = error.normalized_messages()
        # Save log API
        LogApi.save_log(
            _request=request,
            response_json=response_json,
            app="localhost-cashback",
            status_code=400,
        )
        return jsonify(response_json), 400

    # Cashback calculate
    cashback_value: float = cashback_calculate(products_data=schema.get("products"))
    # Send the calculated cashback to the Mais Todos API
    response_api = send_cashback(
        cashback_value=cashback_value, document=schema.get("customer").get("document")
    )
    if response_api.get("error_message", None) is None:
        # Save log API
        LogApi.save_log(
            _request=request,
            response_json={"message": "ok"},
            app="localhost-cashback",
            status_code=200,
        )
        return jsonify({"message": "ok"}), 200
    # Save log API
    LogApi.save_log(
        _request=request,
        response_json=response_api,
        app="localhost-cashback",
        status_code=400,
    )
    return jsonify(response_api), 400
