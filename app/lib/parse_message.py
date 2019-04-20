from email.utils import parseaddr, parsedate_to_datetime

from app.models import db
from app.models.message import Message, EmailAddress, HEADER_ACTIONS

from app.models.contact import Contact


def parse_message(message):
    for header_raw in message.raw_resource['payload']['headers']:
        name = header_raw['name'].lower()
        value = header_raw['value']

        if not name or not value:
            continue

        if name in HEADER_ACTIONS:
            _parse_actions(message, name, value)
        elif name == 'date':
            dt = parsedate_to_datetime(value)
            message.datetime = dt
        elif name == 'subject':
            message.subject = value
    
    db.session.add(message)
    db.session.commit()
    return message


def _parse_actions(message, action, value):
    """Parses Message.raw_resource to populate
    Message, EmailAddress, and MessageEmailAddress tables."""
    if action not in HEADER_ACTIONS:
        return

    # Headers for an EmailAddress object
    entries = value.split(', ')
    for entry in entries:
        name_str, email_str = parseaddr(entry)
        message.add_email_address(
            email_str=email_str.lower(),
            action=action,
            name=name_str)
    return message
