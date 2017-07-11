"""Module to store settings for different environments."""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Set the default configurations."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "bucketlist.db")


class DevelopmentConfig(Config):
    """Set the configurations for the development environment."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "bucketlist.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']


class TestingConfig(Config):
    """Set the configurations for the testing environment."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "test.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']


class ProductionConfig(Config):
    """Set the configurations for the production environment."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///models/bucketlist.db"


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
