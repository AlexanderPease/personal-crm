# Best documentation:
# https://developers.google.com/api-client-library/python/auth/web-app

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from flask import current_app as app
from flask import session
from flask_login import login_user

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


def credentials_from_dict(credentials):
    return Credentials(**credentials)


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
    user = User(google_credentials=credentials_to_dict(creds))
    from app.models import db
    db.session.add(user)
    db.session.commit()
    return user


def auth_credentials():
    """Returns authenticated Google API credentials."""
    creds = None
    if session.get('credentials'):
        creds = Credentials(**session.get('credentials'))

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                GOOGLE_CREDENTIALS,
                SCOPES
            )
            # flow.redirect_uri = 'http://localhost:8000/google-callback'
            creds = flow.run_local_server()
            session['credentials'] = credentials_to_dict(creds)
            user = store_credentials(creds)
            login_user(user, remember=True)
    return creds


def init_service(creds):
    return build('gmail', 'v1', credentials=creds)


def service_for_user(user):
    try:
        return init_service(
            credentials_from_dict(user.google_credentials)
        )
    except Exception:
        pass
