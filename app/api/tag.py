from flask_restful import Resource, reqparse, abort

from app.schema.tag import TagSchema
from app.lib.api import get_or_abort
from app.models.tag import Tag

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


parser = reqparse.RequestParser()
parser.add_argument('id')


class MessageAPI(Resource):
    def get(self, obj_id):
        tag = get_or_abort(Tag, obj_id)
        return tag_schema.dump(tag).data


class MessageListAPI(Resource):
    def get(self):
        tags = Tag.query.all()
        return tags_schema.dump(tags).data
