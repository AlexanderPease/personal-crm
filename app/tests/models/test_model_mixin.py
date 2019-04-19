from nose.tools import assert_equals

from app.models import db
from app.models.message import Message
from app.tests.models import TestModelBase


class TestModelMixin(TestModelBase):
    """Tests ModelMixin methods."""
    model = Message

    def test_get_or_create(self):
        # Basic create
        obj = self.model.get_or_create(message_id='12345')
        assert_equals(obj.id, 1)
        assert_equals(
            len(self.model.query.all()), 1
        )


