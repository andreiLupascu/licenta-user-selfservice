import logging

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

import app.controllers.user as user

mail = Mail()


def create_app():
    app = Flask(__name__)
    Swagger(app)
    CORS(app)
    app.config.from_envvar('FLASK_CONFIG_FILE')
    app.logger.setLevel(logging.DEBUG)
    jwt = JWTManager(app)
    app.register_blueprint(user.app)
    mail.init_app(app)
    return app


if __name__ == "__main__":
    create_app().run(port=5006)
