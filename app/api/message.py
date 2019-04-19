from flask_restful import Resource, reqparse, abort

from app.schema.message import MessageSchema
from app.lib.api import get_or_abort
from app.models.message import Message

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)


parser = reqparse.RequestParser()
parser.add_argument('id')


class MessageAPI(Resource):
    def get(self, obj_id):
        message = get_or_abort(Message, obj_id)
        return message_schema.dump(message).data


class MessageListAPI(Resource):
    def get(self):
        messages = Message.query.all()
        return messages_schema.dump(messages).data
