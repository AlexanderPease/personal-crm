from flask_restful import Resource, reqparse, abort

from app.models.message import Message as _Message


def abort_if_dne(cls, _id):
    if not cls.query.get(_id):
        abort(
            404,
            message=f"{cls.__classname__} {_id} doesn't exist"
        )


parser = reqparse.RequestParser()
parser.add_argument('id')


class Message(Resource):
    def get(self, message_id):
        abort_if_dne(_Message, message_id)
        return TODOS[todo_id]

    def delete(self, message_id):
        abort_if_dne(_Message, message_id)
        # del TODOS[todo_id]
        return '', 204

    def put(self, message_id):
        args = parser.parse_args()
        # task = {'id': args['task']}
        return '', 201


class MessageList(Resource):
    def get(self):
        return _Message.query.all()
