from flask import Blueprint
from flask_restful import Api

from app.api.message import Message, MessageList

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(MessageList, '/message')
api.add_resource(Message, '/message/<message_id>')
