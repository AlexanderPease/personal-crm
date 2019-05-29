from flask import current_app as app
from flask import (
    Blueprint, render_template, redirect, url_for, session)
from flask_login import current_user, login_user, logout_user

from app.lib.google_auth import (
    auth_credentials, service_for_user, credentials_to_dict)
from app.lib.gmail import GmailService
from app.models import db
from app.models.contact import Contact
from app.models.mailbox import Mailbox
from app.models.message import Message, EmailAddress, HEADER_ACTIONS
from app.models.tag import Tag
from app.models.user import User


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
        user = User.query.get(10)  # TODO: garbage
        login_user(user, remember=True)
    return 'Success'


@app.route('/auth/logout')
def logout():
    logout_user()
    session.clear()


QUERY_LIMIT = 100


@app.route('/message')
def messages():
    return render_template(
        'public/messages.html', messages=Message.query.limit(QUERY_LIMIT))


@app.route('/email-address')
def email_addresses():
    return render_template(
        'public/email_addresses.html',
        email_addresses=EmailAddress.query.limit(QUERY_LIMIT),
        header_actions=HEADER_ACTIONS
    )


@app.route('/contact')
def contact():
    return render_template(
        'public/contacts.html',
        contacts=Contact.query.limit(QUERY_LIMIT),
        header_actions=HEADER_ACTIONS
    )


@app.route('/tag')
def tag():
    return render_template(
        'public/tags.html',
        tags=Tag.query.limit(QUERY_LIMIT)
    )
