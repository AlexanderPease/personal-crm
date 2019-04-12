# Base file for initiating flask app
import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from app.config import CONFIG_MAPPING
from app.models import db

# Is this necessary?
# app = Flask(__name__)


###############################################################################
# Config
###############################################################################
def register_config(app):
    # Instantiate app for nose tests
    if os.environ.get('NOSE_TESTS'):
        print('running test config')  # not happening
        app.config.from_object('test')
        return

    # Prod, dev, and local instantiation
    environment = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(
        CONFIG_MAPPING.get(environment)
    )
    app.secret_key = app.config.get('SECRET_KEY')
    app.debug = app.config.get('FLASK_DEBUG')


def register_db(app):
    db.init_app(app)
    Migrate(app, db, compare_type=True)


def register_blueprints(app):
    from app.handlers.public import mod as public_module
    app.register_blueprint(public_module)


def register_extensions(app):
    login_manager = LoginManager()
    # login_manager.login_view = 'login.login'
    # login_manager.refresh_view = 'login.reauthenticate'
    login_manager.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        """Loads active User object for LoginManager."""
        try:
            return User.query.get(user_id)
        except Exception:
            return None


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
        register_extensions(app)

    return app


app = create_app()
