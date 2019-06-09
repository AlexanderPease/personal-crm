from nose.tools import assert_equals, assert_false

from app.lib.email_address import valid_email, clean_email, generate_name
from app.tests import TestBase


class TestLibEmailAddress(TestBase):
    """Tests app/lib/email_address.py functions."""

    def test_valid_email(self):
        invalid_emails = [None, '', 'myraguptagmail.com', 'myra@gmailcom', '@gmail.com']
        for e in invalid_emails:
            assert_false(valid_email(e))

    def test_clean_email(self):
        test_pairs = [
            ('MyraGupta@gmail.com', 'myragupta@gmail.com')
        ]
        for test, cleaned in test_pairs:
            assert_equals(clean_email(test), cleaned)

    def test_generate_name(self):
        test_pairs = [
            ('myra.gupta@gmail.com', 'Myra Gupta'),
            ('fred89@gmail.com', 'Fred')
        ]
        for test, cleaned in test_pairs:
            assert_equals(generate_name(test), cleaned)
