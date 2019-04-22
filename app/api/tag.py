from flask_restful import Resource, reqparse, abort

from app.schema.tag import TagSchema
from app.lib.api import get_or_abort
from app.models.tag import Tag

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


parser = reqparse.RequestParser()


class TagAPI(Resource):
    def get(self, obj_id):
        tag = get_or_abort(Tag, obj_id)
        return tag_schema.dump(tag).data


class TagListAPI(Resource):
    def get(self):
        tags = Tag.query.all()
        return tags_schema.dump(tags).data

    def post(self):
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        name = args.get('name')
        
        tag = Tag.get_or_create(name=name)
        return tag_schema.dump(tag).data
