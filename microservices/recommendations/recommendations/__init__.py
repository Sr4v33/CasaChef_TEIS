from flask import Flask
from flask_cors import CORS

from recommendations.config import Settings
from recommendations.presentation.routes import api_bp, register_error_handlers


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Settings())
    CORS(app)

    app.register_blueprint(api_bp)
    register_error_handlers(app)

    return app
