from marshmallow import Schema, fields


class ContactSchema(Schema):
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
    to_count = fields.Integer()
    to_latest = fields.String()
    from_count = fields.Integer()
    from_latest = fields.String()
