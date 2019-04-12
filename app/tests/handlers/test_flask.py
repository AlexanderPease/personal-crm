from nose.tools import assert_equals

from app import app
from app.tests import TestBase


class TestFlask(TestBase):
    """Basic tests for Flask server."""

    def test_flask(self):
        result = self.app.get('/')
        assert_equals(result.status_code, 200)
