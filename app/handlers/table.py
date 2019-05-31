from flask import current_app as app
from flask import Blueprint, render_template
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import not_

from app.models import db
from app.models.contact import Contact
from app.models.message import (
    Message, EmailAddress, MessageEmailAddress, HEADER_ACTIONS)
from app.models.tag import Tag


mod = Blueprint('table', __name__)


QUERY_LIMIT = 1000


@app.route('/message')
def messages():
    return render_template(
        'table/messages.html', messages=Message.query.limit(QUERY_LIMIT))


@app.route('/email-address')
def email_addresses():

    ea = (
        db.session.query(EmailAddress).
        join(EmailAddress.message_email_address).
        join(MessageEmailAddress.message).
        group_by(EmailAddress.id, EmailAddress.email_address, EmailAddress.name, MessageEmailAddress.action)
    )

    ea = db.session.execute(
        '''
        SELECT
            e.email_address as email_address,
            e.name as name,
            COUNT(*) as "Total",
            COUNT(case when assoc.action = 'from' then 1 ELSE NULL END) as "From",
            MAX(case when assoc.action = 'from' then m.datetime else null end) as "Latest From",
            COUNT(case when assoc.action = 'to' or assoc.action = 'cc' or assoc.action = 'bcc' then 1 ELSE NULL END) as "To",
            MAX(case when assoc.action = 'to' or assoc.action = 'cc' or assoc.action = 'bcc' then m.datetime ELSE NULL END) as "Latest To"

        FROM email_address e
        LEFT JOIN message_email_address assoc
        ON e.id = assoc.email_id

        LEFT JOIN message m
        on m.id = assoc.message_id

        WHERE e.status = 0

        GROUP BY e.email_address, e.name, assoc.action

        LIMIT 1000
        '''
    )

    col_mapping = {
        'email': 0,
        'name': 1,
        'total': 2,
        'from': 3,
        'from_latest': 4,
        'to': 5,
        'to_latest': 6
    }

    return render_template(
        'table/email_address_raw.html',
        email_addresses=ea,
        map=col_mapping
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
