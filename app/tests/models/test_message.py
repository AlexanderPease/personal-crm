from nose.tools import assert_equals

from app import app
from app.models import db
from app.models.message import Message
from app.tests.models import TestModelBase

ITERATIONS = 99


class TestMessage(TestModelBase):
    model = Message

    def test_add(self):
        with self.app.application.app_context():
            message = Message(thread_id=1)
            assert_equals(message.thread_id, 1)
            db.session.add(message)
            db.session.commit()
            assert_equals(
                len(Message.query.all()), 1
            )

    def test_add_multiple(self):
        with self.app.application.app_context():
            for i in range(1, ITERATIONS):
                self.add(message_id=i)

    def test_unique(self):
        with self.app.application.app_context():
            msg_str = '123abc'
            msg = self.add(message_id=msg_str)
            try:
                msg2 = self.add(message_id=msg_str)
                raise  # Should not be able to add to db
            except:
                pass