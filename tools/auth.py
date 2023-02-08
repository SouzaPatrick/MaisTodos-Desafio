import datetime
from functools import wraps
from typing import Optional

import jwt
from flask import jsonify, request

from app.db_function import get_user_by_username
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get("Authorization").lstrip("Bearer").strip()
        except AttributeError:
            return (
                jsonify({"error_message": "The token was not sent in the header"}),
                401,
            )
        if not token:
            return jsonify({"error_message": "Token is missing"}), 401
        try:
            # TODO replace "123" by app.config["SECRET_KEY"]
            data = jwt.decode(token, "123", algorithms=["HS256"])
            current_user = get_user_by_username(username=data["username"])
            if not current_user:
                return jsonify({"error_message": "Token is invalid or expired"}), 401
        except jwt.exceptions.DecodeError:
            return (
                jsonify(
                    {
                        "error_message": "Could not verify",
                        "WWW-Authenticate": "Bearer Token required",
                    }
                ),
                401,
            )
        return f(current_user, *args, **kwargs)

    return decorated


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return (
            jsonify(
                {
                    "error_message": "Could not verify",
                    "WWW-Authenticate": 'Basic auth="Login required"',
                }
            ),
            401,
        )
    user: Optional[User] = get_user_by_username(auth.username)
    if not user:
        return jsonify({"error_message": "User not found"}), 401

    if user and user.verify_password(auth.password):
        token: str = jwt.encode(
            {
                "username": user.username,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=12),
            },
            # TODO replace "123" by app.config["SECRET_KEY"]
            "123",
        )
        return jsonify(
            {
                "message": "Validated successfully",
                "token": token,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=12),
            }
        )

    return (
        jsonify(
            {
                "error_message": "Could not verify",
                "WWW-Authenticate": 'Basic auth="Login required"',
            }
        ),
        401,
    )
