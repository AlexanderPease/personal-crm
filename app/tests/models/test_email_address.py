from nose.tools import assert_equals
from sqlalchemy.exc import IntegrityError

from app import app
from app.models import db
from app.models.message import EmailAddress
from app.tests.models import TestModelBase


class TestEmailAddress(TestModelBase):
    model = EmailAddress

    def test_add(self):
        with self.app.application.app_context():
            # Add first
            email_str = "test@test.com"
            name_str = "Sample Name"
            ea = EmailAddress(email_address=email_str, name=name_str)
            assert_equals(ea.email_address, email_str)
            assert_equals(ea.name, name_str)
            
            db.session.add(ea)
            db.session.commit()
            assert_equals(
                len(EmailAddress.query.all()), 1
            )

    def test_add_multiple(self):
        with self.app.application.app_context():
            for i in range(1, self.iterations):
                self.add(email_address=f'test{i}@test.com')

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
