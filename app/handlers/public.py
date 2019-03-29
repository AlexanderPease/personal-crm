from flask import current_app as app
from flask import (
    Blueprint, jsonify, redirect, render_template, request,
    send_from_directory, session, url_for)

mod = Blueprint('public', __name__)

@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/apply')
def application_email():
    return 'Hello, World!'


@app.route('/apply-2')
def application_full():
    return 'Hello, World!'


@app.route('/apply/success')
def apply():
    return 'Hello, World!'


