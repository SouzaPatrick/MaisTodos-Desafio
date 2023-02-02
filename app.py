from flask import Flask, jsonify, request
from schema import CashbackSchema, configure_app
from marshmallow.exceptions import ValidationError

app = Flask(__name__)
app.debug = True

configure_app(app)

@app.route("/api/cashback", methods=['POST'])
def cashback():
    try:
        errors = CashbackSchema().validate(request.get_json())

        if errors:
            return jsonify(errors), 400
        return jsonify({
                "message": 'ok'
            }), 200
    except ValidationError as error:
        return jsonify(error.normalized_messages()), 400
