from flask import Blueprint
from flask_restful import Api

from app.api.email_address import EmailAddressAPI, EmailAddressListAPI
from app.api.message import MessageAPI, MessageListAPI

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(EmailAddressListAPI, '/email-address')
api.add_resource(EmailAddressAPI, '/email-address/<obj_id>')

api.add_resource(MessageListAPI, '/message')
api.add_resource(MessageAPI, '/message/<obj_id>')
