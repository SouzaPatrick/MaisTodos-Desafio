from typing import Optional

from flask import Flask, jsonify, request
from marshmallow.exceptions import ValidationError

from db_function import get_products
from models import ProductType
from schema import CashbackSchema, configure_app

app = Flask(__name__)
configure_app(app)


def cashback_calculate(products_data: list[dict]) -> float:
    products_type_data: list[str] = []
    for product_data in products_data:
        products_type_data.append(product_data.get("type"))

    products_type: list[ProductType] = get_products(
        products_type_data=products_type_data
    )

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

    return {}


@app.route("/api/cashback", methods=["POST"])
def cashback():
    data: dict = request.get_json()
    try:
        schema: Optional[dict] = CashbackSchema().load(data)
        if schema is None:
            return jsonify(schema), 400
    except ValidationError as error:
        return jsonify(error.normalized_messages()), 400

    # Cashback calculate
    cashback_calculate(products_data=schema.get("products"))
    # TODO Send the calculated cashback to the Mais Todos api
    # response_api: dict = send_cashback(
    #     cashback_value=cashback_value, document=schema.get("customer").get("document")
    # )

    return jsonify({"message": "ok"}), 200
