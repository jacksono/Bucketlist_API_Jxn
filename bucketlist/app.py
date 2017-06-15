"""Module to initialise and configure the flask app and the db."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# initialise flask app
app = Flask(__name__)

# configure and create a db object
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
                                                    basedir, 'bucketlist.db')
db = SQLAlchemy(app)
