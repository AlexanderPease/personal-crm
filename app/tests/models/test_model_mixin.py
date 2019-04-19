from nose.tools import assert_equals

from app import app
from app.models import db
from app.models.message import Message
from app.tests.models import TestModelBase


class TestModelMixin(TestModelBase):
    """Tests ModelMixin methods."""
    model = Message

    def test_get_or_create(self):
        with self.app.application.app_context():
            # Set up unique_kwargs
            message_id = '12345'
            unique_kwargs = dict(message_id=message_id)

            # Basic create
            obj = self.model.get_or_create(**unique_kwargs)
            assert_equals(obj.id, 1)
            assert_equals(obj.message_id, message_id)
            assert_equals(
                len(self.model.query.all()), 1
            )

            # Basic get - should not create a second, idential obj
            obj = self.model.get_or_create(**unique_kwargs)
            assert_equals(obj.id, 1)
            assert_equals(obj.message_id, message_id)
            assert_equals(
                len(self.model.query.all()), 1
            )

            # Set up create_kwargs
            thread_id = 'abcdef'
            create_kwargs = dict(thread_id=thread_id)

            # Fail on create with same unique_kwargs but additional create_kwargs
            obj = self.model.get_or_create(create_kwargs=create_kwargs, **unique_kwargs)
            assert_equals(obj.id, 1)
            assert_equals(
                len(self.model.query.all()), 1
            )

            # Create with additional create_kwargs
            message_id_2 = '67890'
            unique_kwargs_2 = dict(message_id=message_id_2)
            obj = self.model.get_or_create(create_kwargs=create_kwargs, **unique_kwargs_2)
            assert_equals(obj.id, 2)
            assert_equals(obj.thread_id, thread_id)
            assert_equals(
                len(self.model.query.all()), 2
            )

            # Get with additional create_kwargs
            obj = self.model.get_or_create(create_kwargs=create_kwargs, **unique_kwargs_2)
            assert_equals(obj.id, 2)
            assert_equals(obj.thread_id, thread_id)
            assert_equals(
                len(self.model.query.all()), 2
            )

