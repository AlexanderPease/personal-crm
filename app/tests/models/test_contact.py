from nose.tools import assert_equals

from app.models import db
from app.models.contact import Contact
from app.models.tag import Tag
from app.tests.models import TestModelBase


class TestContact(TestModelBase):
    """Tests app/lib/contact.py functions."""
    model = Contact

    def test_instantiate(self):
        c = Contact(
            name='Charlie Work',
            company="TestCo"
        )
        assert_equals(c.name, 'Charlie Work')
        assert_equals(c.company, 'TestCo')

    def test_tags(self):
        with self.app.application.app_context():
            name_str = 'Charlie Work'
            c = Contact(name=name_str)
            assert_equals(c.tags, [])

            db.session.add(c)
            db.session.commit()
            assert_equals(
                len(Contact.query.all()), 1
            )

            # Add tag
            t1 = Tag(name='tag')
            c.tags.append(t1)
            db.session.add(c)
            db.session.commit()
            assert_equals(
                len(c.tags), 1
            )

            # Add second tag
            t2 = Tag(name='tag2')
            c.tags.append(t2)
            assert_equals(
                len(c.tags), 2
            )

            # Fail to add redundant tag
            t3 = Tag(name='tag')
            try:
                c.tags.append(t3)
                raise
            except AssertionError:
                pass
            assert_equals(
                len(c.tags), 2
            )
