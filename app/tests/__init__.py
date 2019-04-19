import os

from app import app
from app.config import TestConfig
from app.models import db


class TestBase:
    """Base class for tests."""
    iterations = 99  # Default number of iterations

    @classmethod
    def setup_class(cls):
        os.environ['NOSE_TESTS'] = 'true'  # not being set...

    def setup(self):
        # Not correctly setting env variables, __init__ isn't getting
        # os.environ['NOSE_TESTS'] = 'true'
        self.app = app.test_client()

        # ...hack around config
        self.app.application.config.from_object(TestConfig)

        with self.app.application.app_context():
            db.create_all()

    def teardown(self):
        with self.app.application.app_context():
            db.drop_all()
