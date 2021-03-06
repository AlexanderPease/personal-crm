from flask import current_app as app
from flask import (
    Blueprint, render_template, redirect, url_for, session)
from flask_login import current_user, login_user, logout_user

from app.lib.google_auth import (
    auth_credentials, service_for_user, credentials_to_dict)
from app.lib.gmail import GmailService
from app.models import db
from app.models.mailbox import Mailbox
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

    return render_template('index.html')


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
