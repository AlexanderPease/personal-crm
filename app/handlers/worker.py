from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from app.lib.gmail import GmailService
from app.lib.parse_messages import parse_message
from app.models import db
from app.models.mailbox import Mailbox
from app.models.message import Message


mod = Blueprint('worker', __name__)


@app.route('/list-messages')
def list_messages():
    """Step 1: Get all message_ids and create placeholder Messages."""
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

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

    return 'Success'


@app.route('/get-message')
def get_message():
    """Step 2: Get full information for all placeholder Messages."""
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    service = GmailService(current_user)
    mailbox = Mailbox.query.filter_by(user_id=current_user.id).first()

    for msg in messages:
        msg = service.get_message(msg['id'])
        message = Message(
            message_id=msg['id'],
            thread_id=msg['threadId'],
            mailbox_id=mailbox.id,
            raw_resource=msg
        )
        db.session.add(message)
        db.session.commit()


@app.route('/parse-messages')
def parse_headers():
    """Step 3: Parse Message headers."""
    messages = Message.query.all()
    for message in messages:
        parse_message(message)

    return 'Success'
