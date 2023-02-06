from flask import Flask
from flask_marshmallow import Marshmallow

ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    ma.init_app(app)

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)
    return app
