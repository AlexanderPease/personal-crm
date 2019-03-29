"""Defines the environment variables to load from prod/dev servers."""
import os


CONFIG_MAPPING = {
    'prod': 'app.config.ProductionConfig',
    'development': 'app.config.LocalConfig',
    'local': 'app.config.LocalConfig'
}


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Degrades app performance


class LocalConfig(Config):
    DEBUG = True
    TESTING = True
    FLASK_LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    FLASK_LOG_LEVEL = 'WARNING'
