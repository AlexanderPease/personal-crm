from nose.tools import assert_equals

from app import app
from app.models.message import Message
from app.tests.models import TestModelBase


class TestMessageAPI(TestModelBase):
    model = Message

    def test_message_list(self):
        result = self.app.get('/api/message')
        assert_equals(result.status_code, 200)

    def test_message(self):
        with self.app.application.app_context():
            result = self.app.get('/api/message/1')
            assert_equals(result.status_code, 404)

            self.add(message_id='12345')
            result = self.app.get('/api/message/1')
            assert_equals(result.status_code, 200)
            assert '"id": 1' in str(result.data)
            assert '"message_id": "12345"' in str(result.data)
