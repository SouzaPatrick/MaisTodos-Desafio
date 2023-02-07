from typing import Optional

from flask import Flask
from flask_marshmallow import Marshmallow
from sqlalchemy.future import Engine

from .database import get_engine

ma = Marshmallow()


def create_app(engine_db: Optional[Engine] = None):
    app = Flask(__name__)
    ma.init_app(app)

    if engine_db is not None:
        app.engine: Engine = engine_db
    else:
        app.engine: Engine = get_engine()

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint)
    return app
