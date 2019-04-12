from nose.tools import assert_equals

from app import app
from app.models import db
from app.models.message import Message
from app.tests import TestBase


class TestMessage(TestBase):

    def test_create(self):
        message = Message(thread_id=1)
        assert_equals(message.thread_id, 1)

        with self.app.application.app_context():
            db.session.add(message)
            db.session.commit()
            assert_equals(
                len(Message.query.all()), 1
            )
