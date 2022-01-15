from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config


def create_app():
    app = Flask(__name__,template_folder='templates', static_folder='./static')
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    return app
