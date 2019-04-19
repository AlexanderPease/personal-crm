from nose.tools import assert_equals

from app import app
from app.models.message import EmailAddress
from app.tests.models import TestModelBase

class TestEmailAddressAPI(TestModelBase):
    model = EmailAddress
    endpoint = 'api/email-address'

    def test_email_address_list(self):
        with self.app.application.app_context():
            for i in range(1, self.iterations):
                self.add(email_address=f'test{i}@test.com')

        result = self.app.get('api/email-address')
        assert_equals(result.status_code, 200)


    def test_email_address(self):
        with self.app.application.app_context():
            endpoint = self.endpoint + '/1'
            
            result = self.app.get(endpoint)
            assert_equals(result.status_code, 404)

            email_str = 'test@test.com'
            self.add(email_address=email_str)
            result = self.app.get(self.endpoint)
            assert_equals(result.status_code, 200)
            assert '"id": 1' in str(result.data)
            assert f'"email_address": "{email_str}"' in str(result.data)
