from email.utils import parseaddr, parsedate_to_datetime

from app.models import db
from app.models.message import Message, EmailAddress, HEADER_ACTIONS

from app.models.contact import Contact

# todo: refactor to only iterate over headers once
def parse_message(message):
    parse_actions(message)
    parse_datetime(message)
    parse_subject(message)


def parse_actions(message):
    """Parses Message.raw_resource to populate
    Message, EmailAddress, and MessageEmailAddress tables."""
    for header_raw in message.raw_resource['payload']['headers']:
        action = header_raw['name'].lower()
        value = header_raw['value']

        if not action or not value or action not in HEADER_ACTIONS:
            continue

        # Headers for an EmailAddress object
        entries = value.split(', ')
        for entry in entries:
            name_str, email_str = parseaddr(entry)
            message.add_email_address(
                email_str=email_str.lower(),
                action=action,
                name=name_str)
    return message


def parse_datetime(message):
    """Parses Message.raw_headers datetime."""
    for header_raw in message.raw_resource['payload']['headers']:
        if header_raw['name'] != "Date":
            continue

        dt_str = header_raw.get('value')
        if not dt_str:
            return

        dt = parsedate_to_datetime(dt_str)
        message.datetime = dt

        db.session.add(message)
        db.session.commit()
    return message



def parse_subject(message):
    """Parses Message.raw_headers subject line."""
    for header_raw in message.raw_resource['payload']['headers']:
        if header_raw['name'] != "Subject":
            continue

        message.subject = header_raw.get('value')

        db.session.add(message)
        db.session.commit()
    return message
