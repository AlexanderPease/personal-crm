# Base file for initiating flask app


# Need to add DB management
# https://medium.com/@dushan14/create-a-web-application-with-python-flask-postgresql-and-deploy-on-heroku-243d548335cc

import os
from flask import Flask

from app.config import CONFIG_MAPPING
from app.models import db

app = Flask(__name__)


###############################################################################
# Config
###############################################################################
def register_config(app):
    environment = os.environ.get('FLASK_ENV', 'development')

    # if app.config.get('TESTING'):
    #     app.config.from_pyfile('config_test.py')

    app.config.from_object(
        CONFIG_MAPPING.get(environment)
    )
    app.secret_key = app.config.get('SECRET_KEY')

    if app.config.get('FLASK_DEBUG'):
        print('app.debug set to True')  # Not being set for some reason...
        app.debug = True


def register_db(app):
    db.init_app(app)


def register_blueprints(app):
    from app.handlers.public import mod as public_module
    app.register_blueprint(public_module)


###############################################################################
# Main app setup
###############################################################################
def create_app():
    # Create Flask app
    app = Flask(__name__)

    # Configure app
    with app.app_context():
        register_config(app)
        register_db(app)
        register_blueprints(app)

    return app


app = create_app()
