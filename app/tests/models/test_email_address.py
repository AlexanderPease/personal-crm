from nose.tools import assert_equals

from app import app
from app.models import db
from app.models.message import EmailAddress
from app.tests.models import TestModelBase

ITERATIONS = 99

class TestEmailAddress(TestModelBase):
    model = EmailAddress

    def test_add(self):
        with self.app.application.app_context():
            # Add first
            email_str = "test@test.com"
            ea = EmailAddress(email_address=email_str)
            assert_equals(ea.email_address, email_str)
            
            db.session.add(ea)
            db.session.commit()
            assert_equals(
                len(EmailAddress.query.all()), 1
            )

    def test_add_multiple(self):
        with self.app.application.app_context():
            for i in range(1, ITERATIONS):
                self.add(email_address=f'test{i}@test.com')

    def test_unique(self):
        with self.app.application.app_context():
            ea = self.add(email_address="test@test.com")
            try:
                ea2 = self.add(email_address="test@test.com")
                raise  # Should not be able to add to db
            except:
                pass
