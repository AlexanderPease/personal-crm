from flask import current_app as app
from flask import Blueprint, render_template
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import not_

from app.models import db
from app.models.contact import Contact
from app.models.message import (
    Message, EmailAddress, MessageEmailAddress, HEADER_ACTIONS,
    EmailAddressProxyTable
)
from app.models.tag import Tag


mod = Blueprint('table', __name__)


QUERY_LIMIT = 1000


@app.route('/message')
def messages():
    return render_template(
        'table/messages.html', messages=Message.query.limit(QUERY_LIMIT))


@app.route('/email-address')
def email_addresses():
    return render_template(
        'table/email_address_raw.html', ea=EmailAddressProxyTable()
    )


@app.route('/contact')
def contact():
    return render_template(
        'table/contacts.html',
        contacts=Contact.query.limit(QUERY_LIMIT),
        header_actions=HEADER_ACTIONS
    )


@app.route('/tag')
def tag():
    return render_template(
        'table/tags.html',
        tags=Tag.query.limit(QUERY_LIMIT)
    )
