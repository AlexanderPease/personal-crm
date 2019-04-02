"""Defines the environment variables to load from prod/dev servers."""
import os


CONFIG_MAPPING = {
    'prod': 'app.config.ProductionConfig',
    'development': 'app.config.DevelopmentConfig',
    'local': 'app.config.LocalConfig'
}


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Degrades app performance

    GOOGLE_CLIENT_ID = '403157355212-1ku5k36ghecsk2591j47qbiaj8ac2u3t.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')


class LocalConfig(Config):
    FLASK_DEBUG = True
    FLASK_LOG_LEVEL = 'DEBUG'

    TESTING = True


class DevelopmentConfig(LocalConfig):
    pass


class ProductionConfig(Config):
    FLASK_LOG_LEVEL = 'WARNING'
