from marshmallow import Schema, fields

from app.models import ma


class TagSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    contacts = fields.Nested(
        'ContactSchema',
        many=True
    )