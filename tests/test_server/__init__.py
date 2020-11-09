from flask import Flask
from http_server_mock import HttpServerMock

from .server import main


def create_app_mock():
    app = HttpServerMock(__name__)

    app.register_blueprint(main)

    return app


def create_app():
    app = Flask(__name__)

    app.register_blueprint(main)

    return app



