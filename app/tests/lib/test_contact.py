from nose.tools import assert_equals

from app.lib.contact import merge_contacts
from app.models.contact import Contact
from app.tests import TestBase


class TestContact(TestBase):
    """Tests app/lib/contact.py functions."""

    def test_clean_name(self):
        c1 = Contact(name="D Shipper")

        c2 = Contact(name="Dan Shipper")

        for test, cleaned in test_pairs:
            assert_equals(clean_name(test), cleaned)
