from typing import Optional

from flask import jsonify, request
from marshmallow.exceptions import ValidationError

from app.models import LogApi, User
from app.schema import CashbackSchema
from tools.auth import auth, token_required
from tools.cashback import cashback_calculate
from tools.mais_todos import send_cashback

from . import api


@api.route("/api/login", methods=["POST"])
def login():
    return auth()


@api.route("/api/cashback", methods=["POST"])
@token_required
def cashback(current_user: User):
    # Verify authotization
    if not current_user.send_cashback:
        return jsonify({"error_message": "User without access permission"}), 403
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
                user=current_user,
                status_code=400,
            )
            return jsonify(response_json), 400
    except ValidationError as error:
        response_json = error.normalized_messages()
        # Save log API
        LogApi.save_log(
            _request=request,
            response_json=response_json,
            user=current_user,
            status_code=400,
        )
        return jsonify(response_json), 400

    # Cashback calculate
    cashback_value: float = cashback_calculate(products_data=schema.get("products"))
    # Send the calculated cashback to the Mais Todos API
    response_api = send_cashback(
        cashback_value=cashback_value,
        document=schema.get("customer").get("document"),
        current_user=current_user,
    )
    if response_api.get("error_message", None) is None:
        response_json = {"message": "success"}
        # Save log API
        LogApi.save_log(
            _request=request,
            response_json=response_json,
            user=current_user,
            status_code=200,
        )
        return jsonify(response_json), 200
    # Save log API
    LogApi.save_log(
        _request=request,
        response_json=response_api,
        user=current_user,
        status_code=400,
    )
    return jsonify(response_api), 400


@api.route("/health-check")
def health_check():
    return jsonify({"message": "success"}), 200
