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
        value = header_raw['value']

        if not action or not value:
            continue

        # Headers for an EmailAddress object
        if action in HEADER_ACTIONS:
            entries = value.split(', ')
            for entry in entries:
                name_str, email_str = parseaddr(entry)
                message.add_email_address(
                    email_str=email_str.lower(),
                    action=action,
                    name=name_str)
        elif action == 'date':
            pass
        elif action == 'subject':
            pass
    return message
