from flask import Flask, render_template

from app.config import Config
from app.routes import api


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(api)

    @app.get("/")
    def index():
        return render_template("index.html")

    return app
