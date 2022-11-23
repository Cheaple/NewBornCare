import os

from flask import Flask

from app.configs import configs
from app.controllers import blueprints
from app.extensions import db, swagger
from app.utils.middleware import jwt_authentication


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('TYPE', 'default')

    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    app.before_request(jwt_authentication)

    # init extensions
    db.init_app(app)
    swagger.init_app(app)

    # register blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app

