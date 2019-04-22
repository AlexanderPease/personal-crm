from flask import Blueprint
from flask_restful import Api

from app.api.contact import ContactAPI, ContactListAPI
from app.api.email_address import EmailAddressAPI, EmailAddressListAPI
from app.api.message import MessageAPI, MessageListAPI
from app.api.tag import TagAPI, TagListAPI

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(ContactListAPI, '/contact')
api.add_resource(ContactAPI, '/contact/<obj_id>')

api.add_resource(EmailAddressListAPI, '/email-address')
api.add_resource(EmailAddressAPI, '/email-address/<obj_id>')

api.add_resource(MessageListAPI, '/message')
api.add_resource(MessageAPI, '/message/<obj_id>')

api.add_resource(TagListAPI, '/tag')
api.add_resource(TagAPI, '/tag/<obj_id>')
