from nose.tools import assert_equals

from app.lib.contact import merge_contacts
from app.models import db
from app.models.contact import Contact
from app.models.message import EmailAddress
from app.models.tag import Tag
from app.models.mixins.status_mixin import OBJECT_STATUS_DELETED
from app.tests import TestBase


class TestContact(TestBase):
    """Tests app/lib/contact.py functions."""

    def test_merge_contacts(self):
        with self.app.application.app_context():
            c1 = Contact(name="Dan Shipper")
            c2 = Contact(name="D Shipper")

            # Set up email addresses
            e1 = EmailAddress(email_address="1@test.com")
            e1.contact = c1
            e2 = EmailAddress(email_address="2@test.com")
            e2.contact = c2
            db.session.add_all([e1, e2])

            # Set up tags
            t1 = Tag(name="t1")
            c1.tags.append(t1)
            t2 = Tag(name="t2")
            c2.tags.append(t1)  # redundant tag
            c2.tags.append(t2)  # non-redundant tag
            db.session.add_all([c1, c2])

            db.session.commit()

            # Merge
            c_merged = merge_contacts(c1, c2)
            assert_equals(c_merged.id, c1.id)
            assert_equals(c_merged.name, "Dan Shipper")

            # Check email addresses
            assert_equals(c_merged, e1.contact)
            assert_equals(c_merged, e2.contact)
            assert_equals(len(c_merged.email_addresses), 2)

            # Check tags
            assert_equals(len(c_merged.tags), 2)
            assert("t2" in list(map(lambda t: t.name, c_merged.tags)))

            # C2 should be "deleted"
            assert_equals(c2.obj_status, OBJECT_STATUS_DELETED)
