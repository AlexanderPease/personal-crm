from flask_restful import Resource, reqparse, abort

from app.lib.api import get_or_abort
from app.lib.constants import EMAIL_STATUS_NORMAL
from app.schema.email_address import EmailAddressSchema
from app.models.message import EmailAddress

schema = EmailAddressSchema()
schema_many = EmailAddressSchema(many=True)


parser = reqparse.RequestParser()
parser.add_argument('id')


class EmailAddressAPI(Resource):
    def get(self, obj_id):
        email_address = get_or_abort(EmailAddress, obj_id)
        return schema.dump(email_address).data


class EmailAddressListAPI(Resource):
    def get(self):
        email_addresses = EmailAddress.query.filter_by(
            status=EMAIL_STATUS_NORMAL).all()
        return schema_many.dump(email_addresses)
