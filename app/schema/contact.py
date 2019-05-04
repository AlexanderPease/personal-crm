from marshmallow import Schema, fields

from app.models import ma
from app.schema import EMAIL_SIMPLE_SCHEMA_ONLY


class ContactSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    company = fields.String()
    email_addresses = fields.Nested(
        'EmailAddressSchema',
        only=('id', 'email_address',),
        many=True
    )
    tags = fields.Nested(
        'TagSchema',
        only=('id', 'name',),
        many=True
    )