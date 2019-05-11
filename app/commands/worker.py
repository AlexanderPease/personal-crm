import click
from flask import current_app as app
from sqlalchemy.sql import not_

from app.lib.gmail import GmailService
from app.lib.parse_message import parse_message
from app.lib.constants import (
    BLACKLIST_EMAIL_SUBSTRINGS, EMAIL_STATUS_IGNORE, EMAIL_STATUS_NORMAL
)
from app.models import db
from app.models.contact import Contact
from app.models.mailbox import Mailbox
from app.models.message import Message, EmailAddress
from app.models.user import User


@app.cli.command('list-messages')
def list_messages():
    """Step 1: Get all message_ids and create placeholder Messages."""
    current_user = User.query.filter_by(email='me@alexanderpease.com').one()

    service = GmailService(current_user)
    mailbox = Mailbox.query.filter_by(user_id=current_user.id).first()

    messages = service.list_messages()

    if not messages:
        print('Service did not find any messages')
        return 'Failure'

    for msg in messages:
        message = Message.get_or_create(
            message_id=msg['id'],
            create_kwargs=dict(
                thread_id=msg['threadId'],
                mailbox_id=mailbox.id
            )
        )
        try:
            db.session.add(message)
            db.session.commit()
        except Exception:
            print(f"Failed to create new Message {msg['id']}")

    print('Success')


@app.cli.command('get-messages')
@click.option('--dry-run', is_flag=True, default=False)
def get_messages(dry_run):
    """Step 2: Get full information for all placeholder Messages."""
    user = User.query.filter_by(email='me@alexanderpease.com').one()

    service = GmailService(user)
    mailbox = Mailbox.query.filter_by(user_id=user.id).first()
    messages = Message.query.filter_by(
        raw_resource=None,
        mailbox=mailbox
    ).all()
    print('Retrieved messages...')

    for i, msg in enumerate(messages):
        print(f'Getting {msg.id}...')
        raw_msg = service.get_message(msg.message_id)
        msg.raw_resource = raw_msg
        db.session.add(msg)
        if i % 100 == 0 and not dry_run:
            db.session.commit()
            print('Committed to db...')

    print('Success')


@app.cli.command('parse-messages')
@click.option('--dry-run', is_flag=True, default=False)
def parse_messages(dry_run):
    """Step 3: Parse Message headers."""
    # Messages without associated EmailAddresses
    has_results = True
    while has_results:
        has_results = False

        query = db.session.query(Message).\
            join(Message.message_email_address, isouter=True).\
            filter(not_(Message.message_email_address.any()))

        for msg in query.limit(100):
            print(f'Parsing {msg.id}...')
            if not dry_run:
                parse_message(msg)
            has_results = True

    print('Success')


@app.cli.command('blacklist-emails')
@click.option('--dry-run', is_flag=True, default=False)
def blacklist_emails(dry_run):
    """Step 4: Ignore certain emails."""
    for substring in BLACKLIST_EMAIL_SUBSTRINGS:
        ea = db.session.query(EmailAddress).filter(EmailAddress.email_address.ilike(substring))
        print(f'Retrieved email addresses for {substring}...')

        if dry_run:
            print(ea.all())
        else:
            ea.update(values={EmailAddress.status: EMAIL_STATUS_IGNORE}, synchronize_session=False)
            db.session.commit()

    print('Success')


@app.cli.command('generate-contacts')
@click.option('--dry-run', is_flag=True, default=False)
def generate_contacts(dry_run):
    """Step 5: Generate Contacts for each EmailAddress."""
    emails = EmailAddress.query.filter_by(status=EMAIL_STATUS_NORMAL, contact=None).all()
    print(f'Retrieved email addresses w/out contacts..')

    for ea in emails:
        if dry_run:
            print(ea)
        else:
            contact = Contact(name=ea.name)
            ea.contact = contact
            db.session.add(ea)
            db.session.commit()

    print('Success')
