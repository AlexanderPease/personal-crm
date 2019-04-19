from marshmallow import Schema, fields

from app.models import ma
from app.schema import EMAIL_SIMPLE_SCHEMA, EMAIL_SIMPLE_SCHEMA_ONLY


# NB: ModelSchema doesn't play nice with relationships
class MessageSchema(ma.Schema):
    id = fields.Integer()
    mailbox = fields.String()
    message_id = fields.String()
    thread_id = fields.String()
    from_ = fields.Nested(
        'EmailAddressSchema',
        attribute='from_email_address',
        only=EMAIL_SIMPLE_SCHEMA_ONLY
    )
    to = fields.Nested(
        'EmailAddressSchema',
        attribute='_email_addresses_to',
        **EMAIL_SIMPLE_SCHEMA
    )
    cc = fields.Nested(
        'EmailAddressSchema',
        attribute='_email_addresses_cc',
        **EMAIL_SIMPLE_SCHEMA
    )
    bcc = fields.Nested(
        'EmailAddressSchema',
        attribute='_email_addresses_bcc',
        **EMAIL_SIMPLE_SCHEMA
    )
    delivered_to = fields.Nested(
        'EmailAddressSchema',
        attribute='_email_addresses_delivered_to',
        **EMAIL_SIMPLE_SCHEMA
    )