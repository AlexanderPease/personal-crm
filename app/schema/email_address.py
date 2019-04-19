from marshmallow import Schema, fields

from app.models import ma
from app.schema import MESSAGE_SIMPLE_SCHEMA


class EmailAddressSchema(ma.Schema):
    id = fields.Integer()
    email_address = fields.String()
    name = fields.String()
    from_ = fields.Nested(
        'MessageSchema',
        attribute='_messages_from',
        **MESSAGE_SIMPLE_SCHEMA
    )
    to = fields.Nested(
        'MessageSchema',
        attribute='_messages_to',
        **MESSAGE_SIMPLE_SCHEMA
    )
    cc = fields.Nested(
        'MessageSchema',
        attribute='_messages_cc',
        **MESSAGE_SIMPLE_SCHEMA
    )
    bcc = fields.Nested(
        'MessageSchema',
        attribute='_messages_bcc',
        **MESSAGE_SIMPLE_SCHEMA
    )
    delivered_to = fields.Nested(
        'MessageSchema',
        attribute='_messages_delivered_to',
        **MESSAGE_SIMPLE_SCHEMA
    )