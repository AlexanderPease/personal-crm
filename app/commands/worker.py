import click
from flask import current_app as app

from app.lib.gmail import GmailService
from app.models import db
from app.models.user import User
from app.models.mailbox import Mailbox
from app.models.message import Message


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
        except:
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
def parse_messages():
    """Step 3: Parse Message headers."""
    messages = Message.query.filter_by(_email_addresses=None).all()
    for msg in messages:
        print(f'Parsing {msg.id}...')
        parse_message(msg)

    print('Success')
