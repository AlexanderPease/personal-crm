from sqlalchemy.orm.exc import NoResultFound
from email.utils import parseaddr

from app.models import db
from app.models.message import Message, EmailAddress, MessageEmailAddress

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


        if name == 'from':
            name_str, email_str = parseaddr(value)
            try:
                email_address = EmailAddress.query.filter_by(
                    email_address=email_str).one()
            except NoResultFound:
                email_address = EmailAddress(email_address=email_str)
                db.session.add(email_address)
                db.session.commit()

            # Can only be a single From: per message
            kwargs = dict(message_id=message.id, action='from')
            try:
                MessageEmailAddress.query.filter_by(**kwargs).one()
            except NoResultFound:
                new_from = MessageEmailAddress(
                    email_id=email_address.id, **kwargs
                )
                db.session.add(new_from)
                db.session.commit()
        elif name == 'to':
            pass
        elif name == 'cc':
            pass
        elif name == 'bcc':
            pass
        elif name == 'delivered-to':
            pass
        elif name == 'date':
            pass
        elif name == 'subject':
            pass


# def parse_from(value):
#     return parseaddr(value)
