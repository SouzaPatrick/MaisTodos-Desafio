from typing import Optional

from flask import jsonify, request
from marshmallow.exceptions import ValidationError

from app import create_app
from app.models import LogApi
from app.schema import CashbackSchema
from tools.cashback import cashback_calculate
from tools.mais_todos import send_cashback

app = create_app()


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
