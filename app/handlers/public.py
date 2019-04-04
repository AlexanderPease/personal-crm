from flask import current_app as app
from flask import (
    Blueprint, render_template, redirect, url_for, session)
from flask_login import current_user, login_user, logout_user

from app.lib.google_auth import (
    auth_credentials, service_for_user, credentials_to_dict)
from app.lib.gmail import GmailService
from app.lib.parse_messages import parse_message
from app.models import db
from app.models.user import User
from app.models.mailbox import Mailbox
from app.models.message import Message, EmailAddress, MessageEmailAddress
from app.models.contact import Contact


mod = Blueprint('public', __name__)


@app.route('/')
def index():
    if current_user.is_authenticated:
        service = service_for_user(current_user)
        if service:
            results = service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])

            if not labels:
                print('No labels found.')
            else:
                print('Labels:')
                for label in labels:
                    print(label['name'])

    return render_template('public/index.html')


@app.route('/auth/google')
def auth():
    """Authenticate with Google Auth API."""
    credentials = auth_credentials()
    if not credentials:
        # to-do failure
        return redirect(url_for('index'))
    creds = credentials_to_dict(credentials)

    if current_user.is_authenticated:
        user = User.query.get(id=current_user.get_id())
        user.google_credentials = creds
        db.session.add(user)
        db.session.commit()
    else:
        # Create User
        user = User(google_credentials=creds)
        service = GmailService(user)
        user.email = service.get_email_address()
        if not user.email:
            # to-do failure
            return redirect(url_for('index'))

        db.session.add(user)
        db.session.commit()

        # Log in
        session['credentials'] = creds
        login_user(user, remember=True)

        # Create associated Gmail inbox
        mailbox = Mailbox(
            user_id=user.id,
            email_address=user.email)

        db.session.add(mailbox)
        db.session.commit()


    return redirect(url_for('index'))


@app.route('/auth/login')
def login():
    if not current_user.is_authenticated:
        user = User.query.get(10) # garbage
        login_user(user, remember=True)
    return 'Success'


@app.route('/auth/logout')
def logout():
    logout_user()
    session.clear()


@app.route('/gmail')
def get_messages():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    service = GmailService(current_user)
    mailbox = Mailbox.query.filter_by(user_id=current_user.id).first()
    
    messages = service.list_messages()

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

    return 'Success'


@app.route('/parse')
def parse_headers():
    messages = Message.query.all()
    for message in messages:
        parse_message(message)

    return 'Success'


@app.route('/messages')
def messages():    
    return render_template('public/messages.html', messages=Message.query.all())


@app.route('/emails')
def emails():
    return render_template('public/email_addresses.html', email_addresses=EmailAddress.query.all())

