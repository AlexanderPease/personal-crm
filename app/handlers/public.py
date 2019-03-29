from flask import current_app as app
from flask import (
    Blueprint, jsonify, redirect, render_template, request,
    send_from_directory, session, url_for)


from app.lib.google_auth import auth_flow


mod = Blueprint('public', __name__)


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/apply')
def application_email():
    return 'Hello, World!'


@app.route('/google')
def google():
    auth_flow()
