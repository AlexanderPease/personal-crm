from marshmallow import Schema, fields


class TagSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    contacts = fields.Nested(
        'ContactSchema',
        exclude=('tags',),
        many=True
    )
