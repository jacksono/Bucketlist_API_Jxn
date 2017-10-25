"""Module to initialise and configure the flask app and the db."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configuration.config import app_config
from flask_restful import Api
from flasgger import Swagger
# from flask.ext.heroku import Heroku


app = Flask(__name__)
app.config.from_object(app_config["development"])
db = SQLAlchemy(app)

# def create_app(configuration):
#     """Initialise and cofigure the app and db."""
#     app = Flask(__name__)
#     app.config.from_object(app_config[configuration])
#     db.init_app(app)
#     return app


template = {
  "swagger": "2.0",
  "info": {
    "title": "BUCKETLIST API",
    "description": "API for managing your bucketlists",
    "contact": {
      "responsibleDeveloper": "Jackson Onyango",
      "email": "jackson.onyango@andela.com",
    },
    "version": "1.0"
  },
  "schemes": [
    "http",
    "https"
  ],
  "produces": ["application/x-www-form-urlencoded",
               "application/json",
               "application/txt"],
  "operationId": "getmyData",
  "content-type": "text"
}

# heroku = Heroku(app)
api = Api(app=app, prefix="/api/v1")
swagger = Swagger(app, template=template)
