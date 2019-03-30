from flask import current_app as app
from flask import (
    Blueprint, render_template, redirect, url_for)
from flask_login import current_user

from app.lib.google_auth import (
    auth_credentials, service_for_user)
from app.lib.gmail import GmailService


mod = Blueprint('public', __name__)


@app.route('/')
def index():
    if current_user.is_authenticated:
        service = service_for_user(current_user)

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


@app.route('/gmail')
def get_messages():
    if current_user.is_authenticated:
        service = GmailService(current_user)
        messages = service.list_messages()
        for msg in messages[0:1]:
            message = service.get_message(msg['id'])

            # print('Message snippet: %s' % message['snippet'])
            for header in message['payload']['headers']:
                print('{}: {}'.format(header['name'], header['value']))
                print('---------')

    return 'Success'
