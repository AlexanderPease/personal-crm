from nose.tools import assert_equals
from sqlalchemy.exc import IntegrityError

from app import app
from app.lib.constants import EMAIL_STATUS_NORMAL
from app.models import db
from app.models.message import EmailAddress
from app.tests.models import TestModelBase


class TestEmailAddress(TestModelBase):
    model = EmailAddress

    def test_instantiate(self):
        """Tests instantiation, including malformed attempts."""
        ea = EmailAddress('test@test.com')
        assert_equals('test@test.com', ea.email_address)

        for ea_bad in ['foo.com', 'foo@com', '@foo.com', 'foo', '']:
            try:
                ea = EmailAddress(ea_bad)
            except ValueError:
                pass
            else:
                raise Exception(
                    f'Instantiated malformed email address: {ea_bad}')

    def test_add(self):
        with self.app.application.app_context():
            # Add first
            email_str = "test@test.com"
            name_str = "Sample Name"
            ea = EmailAddress(email_address=email_str, name=name_str)
            assert_equals(ea.email_address, email_str)
            assert_equals(ea.name, name_str)
            assert_equals(ea.status, EMAIL_STATUS_NORMAL)
            
            db.session.add(ea)
            db.session.commit()
            assert_equals(
                len(EmailAddress.query.all()), 1
            )

    def test_add_multiple(self):
        with self.app.application.app_context():
            for i in range(0, self.iterations):
                self.add(email_address=f'test{i}@test.com')
            assert_equals(
                len(EmailAddress.query.all()), self.iterations
            )

    def test_add_idempotent(self):
        with self.app.application.app_context():
            self.add(email_address=f'test@test.com')
            try:
                self.add(email_address=f'test@test.com')
            except IntegrityError:
                db.session.rollback()
            assert_equals(
                len(EmailAddress.query.all()), 1
            )

    def test_unique(self):
        with self.app.application.app_context():
            ea = self.add(email_address="test@test.com")
            try:
                ea2 = self.add(email_address="test@test.com")
                raise  # Should not be able to add to db
            except:
                pass

    def test_messages(self):
        with self.app.application.app_context():
            self.add(email_address='test@test.c')
