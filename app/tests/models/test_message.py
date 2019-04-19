from nose.tools import assert_equals

from app import app
from app.models import db
from app.models.message import Message, EmailAddress, MessageEmailAddress
from app.tests.models import TestModelBase


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
            for i in range(1, self.iterations):
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

    def test_add_email_address(self):
        """Tests adding associated email addresses."""
        with self.app.application.app_context():
            msg = self.add(message_id=1)

            # Malformed action
            msg.add_email_address('test@test.com', 'FOO')
            assert_equals(
                len(MessageEmailAddress.query.all()), 0
            )

            # From and EmailAddress.name
            msg.add_email_address('from@test.com', 'from', name='From Name')
            assert_equals(msg.from_email_address.email_address, 'from@test.com')
            assert_equals(msg.from_email_address.name, 'From Name')

            # To
            msg.add_email_address('to@test.com', 'to')
            assert_equals(msg.email_addresses('to')[0].email_address, 'to@test.com')
            msg.add_email_address('to_2@test.com', 'to')
            assert_equals(
                len(msg.email_addresses('to')), 2)

            # Idempotent
            msg.add_email_address('to@test.com', 'to')
            assert_equals(
                len(msg.email_addresses('to')), 2
            )
            assert_equals(
                len(EmailAddress.query.filter_by(email_address='to@test.com').all()), 1
            )

            # Same email, different actions
            msg.add_email_address('from@test.com', 'to')
            assert_equals(
                len(msg.email_addresses('to')), 3)
