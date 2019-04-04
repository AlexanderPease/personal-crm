from email.utils import parseaddr

from app.models import db
from app.models.message import Message, EmailAddress, HEADER_ACTIONS

def parse_message(message):
    """Parses Message.raw_headers to populate
    Message, EmailAddress, and MessageEmailAddress tables."""
    for header_raw in message.raw_resource['payload']['headers']:
        # print('{}: {}'.format(header['name'], header['value']))
        # print('---------')
        name = header_raw['name'].lower()
        value = header_raw['value'].lower()

        if not name or not value:
            continue

        # Headers for an EmailAddress object
        if name in HEADER_ACTIONS:
            name_str, email_str = parseaddr(value)
            message.add_email_address(email_str, name)


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
        elif name == 'date':
            pass
        elif name == 'subject':
            pass


# def parse_from(value):
#     return parseaddr(value)
