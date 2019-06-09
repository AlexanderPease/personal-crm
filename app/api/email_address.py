from flask_restful import Resource, reqparse

from app.lib.api import get_or_abort
from app.lib.constants import EMAIL_STATUS_NORMAL
from app.schema.email_address import (
    EmailAddressSchema, EmailAddressProxyTableSchema)
from app.models.message import (
    EmailAddress, EmailAddressProxyTable)

schema = EmailAddressSchema()
schema_many = EmailAddressProxyTableSchema(many=True)


parser = reqparse.RequestParser()
parser.add_argument('id')


class EmailAddressAPI(Resource):
    def get(self, obj_id):
        email_address = get_or_abort(EmailAddress, obj_id)
        return schema.dump(email_address).data


class EmailAddressListAPI(Resource):
    def get(self):
        email_addresses = EmailAddressProxyTable()
        return schema_many.dump(email_addresses)
