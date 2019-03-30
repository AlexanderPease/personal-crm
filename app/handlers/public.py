from flask import current_app as app
from flask import (
    Blueprint, render_template, redirect, url_for)
from flask_login import current_user

from app.lib.google_auth import (
    auth_credentials, init_service, credentials_from_dict)


mod = Blueprint('public', __name__)


@app.route('/')
def index():
    if current_user.is_authenticated:
        service = init_service(
            credentials_from_dict(current_user.google_credentials)
        )
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])

    return render_template('public/index.html')


@app.route('/auth')
def auth():
    # from flask import session
    # session.clear()
    auth_credentials()
    return redirect(url_for('index'))
