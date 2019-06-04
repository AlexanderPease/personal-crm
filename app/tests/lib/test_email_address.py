from nose.tools import assert_equals, assert_false

from app.lib.email_address import valid_email, clean_email
from app.tests import TestBase


class TestLibEmailAddress(TestBase):
    """Tests app/lib/email_address.py functions."""

    def test_valid_email(self):
        invalid_emails = [None, '', 'myraguptagmail.com', 'myra@gmailcom', '@gmail.com']
        for e in invalid_emails:
            assert_false(valid_email(e))

    def test_clean_email(self):
        test_pairs = [
            ('myra.gupta@gmail.com', 'myragupta@gmail.com'),
            ('MyraGupta@gmail.com', 'myragupta@gmail.com')
        ]
        for test, cleaned in test_pairs:
            assert_equals(clean_email(test), cleaned)
