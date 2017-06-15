"""Module to initialise and configure the flask app and the db."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configuration.config import app_config
from flask_restful import Api

db = SQLAlchemy()


def create_app(configuration):
    """Initialise and cofigure the app and db."""
    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    db.init_app(app)
    return app


app = create_app("development")
api = Api(app=app, prefix="/api/v1")
