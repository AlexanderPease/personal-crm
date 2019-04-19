from nose.tools import assert_equals

from app import app
from app.tests import TestBase


class TestEmailAddressAPI(TestBase):

    def test_email_address_list(self):
        result = self.app.get('/api/email-address')
        assert_equals(result.status_code, 200)