from nose.tools import assert_equals

from app.lib.clean import clean_name
from app.tests import TestBase


class TestClean(TestBase):
    """Tests app/lib/clean.py functions."""

    def test_clean_name(self):
        test_pairs = [
            (None, None),
            ('', None),
            ('"Zander Pease"', 'Zander Pease'),
            ("'Zander Pease'", 'Zander Pease')

        ]

        for test, cleaned in test_pairs:
            assert_equals(clean_name(test), cleaned)
