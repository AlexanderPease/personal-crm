from flask_restful import Resource, reqparse, abort
from sqlalchemy.orm.exc import NoResultFound

from app.schema.contact import ContactSchema
from app.lib.api import get_or_abort
from app.lib.contact import merge_contacts
from app.models import db
from app.models.contact import Contact, ContactProxyTable
from app.models.tag import Tag

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


parser = reqparse.RequestParser()


class ContactAPI(Resource):
    def get(self, obj_id):
        contact = get_or_abort(Contact, obj_id)
        return contact_schema.dump(contact).data

    def put(self, obj_id):
        print('PUTTTTT')
        contact = get_or_abort(Contact, obj_id)

        parser.add_argument('name')
        parser.add_argument('company')
        parser.add_argument('tag_id', type=int)
        parser.add_argument('merge', type=int)
        args = parser.parse_args()
        print(args)

        # Merging supercedes other operations
        if args.get('merge', False):
            print('in merge')
            c2 = get_or_abort(Contact, args.get('merge'))
            merge_contacts(contact, c2)

            contacts = ContactProxyTable()
            return contact_schema.dump(contact).data

        # Basic fields
        contact.name = args.get('name', contact.name)
        contact.company = args.get('company', contact.company)

        # Add Tags
        tag_id = args.get('tag_id')
        if tag_id:
            try:
                tag = Tag.query.get(tag_id)
            except NoResultFound:
                abort(404, message=f"Tag {tag_id} doesn't exist")
            try:
                contact.tags.append(tag)
            except AssertionError:
                print(f'Tag {tag.name} already assigned to Contact {contact.id}')
                pass
            db.session.add(tag)

        db.session.commit()

        return contact_schema.dump(contact).data


class ContactListAPI(Resource):
    def get(self):
        contacts = ContactProxyTable()
        return contacts_schema.dump(contacts).data
