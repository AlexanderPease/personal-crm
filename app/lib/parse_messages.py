from email.utils import parseaddr

from app.models.message import Message, EmailAddress, MessageEmailAddress

def parse_message_headers(message):
    """Parses Message.raw_headers to populate
    Message, EmailAddress, and MessageEmailAddress tables."""
    for header_raw in message.raw_headers['payload']['headers']:
        # print('{}: {}'.format(header['name'], header['value']))
        # print('---------')
        name = header_raw['name'].lower()
        value = header_raw['value']

        if not name or not value:
            continue

        if name == 'from':
            realname, email = parse_addr(value)

            try:
                email_address = EmailAddress.query.filter(
                    email_address=email).one()
            except EmailAddress.NoResultFound:
                email_address = EmailAddress(email_address=email)
                db.session.add(email_address)
                db.session.commit()

            new_header = MessageEmailAddress(
                message_id=message.id,
                email_id=email_address.id,
                action='from'
            )
            db.session.add(new_header)
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
