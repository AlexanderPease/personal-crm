"""Defines the environment variables to load from prod/dev servers."""
import os


CONFIG_MAPPING = {
    'prod': 'app.config.ProductionConfig',
    'development': 'app.config.DevelopmentConfig',
    'local': 'app.config.LocalConfig',
    'test': 'app.config.TestConfig'
}


class Config(object):
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids degrade in app performance

    GOOGLE_CLIENT_ID = '403157355212-1ku5k36ghecsk2591j47qbiaj8ac2u3t.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')


class LocalConfig(Config):
    FLASK_DEBUG = True
    FLASK_LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_ECHO = True

    TESTING = True


class DevelopmentConfig(LocalConfig):
    pass


class ProductionConfig(Config):
    FLASK_LOG_LEVEL = 'WARNING'


class TestConfig(object):
    FLASK_ENV = 'test'
    SECRET_KEY = '1234567890'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/crm-test'

    TESTING = True
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
