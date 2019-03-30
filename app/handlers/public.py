from flask import current_app as app
from flask import Blueprint, render_template
# from flask import jsonify, redirect, session, url_for


from app.lib.google_auth import auth_flow


mod = Blueprint('public', __name__)


@app.route('/')
def index():

    from app.models.user import User
    from app.models import db

    user = User(email='test@test.com')
    db.session.add(user)
    db.session.commit()

    return render_template('public/index.html')


@app.route('/google')
def google():
    auth_flow()

    return 'Auth Success!'
