from email.utils import parseaddr

from app.models import db
from app.models.message import Message, EmailAddress, HEADER_ACTIONS

def parse_message(message):
    """Parses Message.raw_headers to populate
    Message, EmailAddress, and MessageEmailAddress tables."""
    for header_raw in message.raw_resource['payload']['headers']:
        # print('{}: {}'.format(header['name'], header['value']))
        # print('---------')
        action = header_raw['name'].lower()
        value = header_raw['value'].lower()

        if not action or not value:
            continue

        # Headers for an EmailAddress object
        if action in HEADER_ACTIONS:
            entries = value.split(', ')
            for entry in entries:
                name_str, email_str = parseaddr(entry)
                message.add_email_address(
                    email_str=email_str,
                    action=action,
                    name=name_str)


        # if name == 'from':
        #     email_address = EmailAddress.get_or_create(email_str)
        #     if not message._from_email:
        #         message._from_email = email_address
        #         db.session.add(message)
        #         db.session.commit()

        #     # Can only be a single From: per message
        #     # kwargs = dict(message_id=message.id, action='from')
        #     # try:
        #     #     MessageEmailAddress.query.filter_by(**kwargs).one()
        #     # except NoResultFound:
        #     #     new_from = MessageEmailAddress(
        #     #         email_id=email_address.id, **kwargs
        #     #     )
        #     #     db.session.add(new_from)
        #     #     db.session.commit()

        # elif name == 'to':
        #     # To: is a string of comma-delimited addresses
        #     addresses = value.split(', ')
        #     for address in addresses:
        #         name_str, email_str = parseaddr(address)
        #         email_address = EmailAddress.get_or_create(email_str)
        #         message.add_to_email(email_address)

        # elif name == 'cc':
        #     pass
        # elif name == 'bcc':
        #     pass
        # elif name == 'delivered-to':
        #     pass
        elif action == 'date':
            pass
        elif action == 'subject':
            pass


# def parse_from(value):
#     return parseaddr(value)
