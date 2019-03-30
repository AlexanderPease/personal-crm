# Best documentation:
# https://developers.google.com/api-client-library/python/auth/web-app

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from flask import current_app as app
from flask import session

from app.models.user import User


GOOGLE_CREDENTIALS = {
    "installed": {
        "client_id": app.config.get('GOOGLE_CLIENT_ID'),
        "client_secret": app.config.get('GOOGLE_CLIENT_SECRET'),
        "project_id": "quickstart-1548690185997",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
}

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


def store_credentials(creds):
    print('store_credenials')
    user = User(google_credentials=credentials_to_dict(creds))
    from app.models import db
    db.session.add(user)
    db.session.commit()
    print('finished')
    return user


def auth_flow():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # if session.get('credentials'):
    #     creds = Credentials(**session.get('credentials'))

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print(GOOGLE_CREDENTIALS)
            flow = InstalledAppFlow.from_client_config(
                GOOGLE_CREDENTIALS,
                SCOPES
            )
            # flow.redirect_uri = 'http://localhost:8000/google-callback'
            creds = flow.run_local_server()
            print(creds)
            print(type(creds))
            print(credentials_to_dict(creds))
            session['credentials'] = credentials_to_dict(creds)
            print(session)
            store_credentials(creds)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])    