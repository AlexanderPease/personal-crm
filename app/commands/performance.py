import click
import time
from flask import current_app as app
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import not_

from app.lib.parse_message import parse_message
from app.models import db
from app.models.contact import Contact
from app.models.mailbox import Mailbox
from app.models.message import Message, EmailAddress
from app.models.user import User


RESULT_LIMIT = 50


@app.cli.command('join-performance')
@click.option('--show-sql', is_flag=True, default=False)
@click.option('--show-results', is_flag=True, default=False)
def join_performance(show_sql, show_results):
    """Test join performance"""
    queries = [
        (
            'Join MessageEmailAddress',
            db.session.query(Message).
            join(Message.message_email_address, isouter=True).
            filter(not_(Message.message_email_address.any()))
        ),
        (
            'Join EmailAddress',
            db.session.query(Message).
            join(Message._email_addresses, isouter=True).
            filter(not_(Message._email_addresses.any()))
        ),
        # Insanely slow
        # (
        #     'Joined Load',
        #     db.session.query(Message).
        #     options(joinedload(Message._email_addresses)).
        #     filter(Message._email_addresses==None)
        # ),
        # (
        #     'Joined Load 2',
        #     db.session.query(Message).
        #     options(joinedload(Message._email_addresses)).
        #     filter_by(_email_addresses=None)
        # ),
    ]

    for query in queries:
        print(f'Testing {query[0]}...')

        start = time.time()
        if show_sql:
            print(f'SQL: {query[1]}')

        results = query[1]
        print(f'{query[0]}: {time.time() - start}')
        print(f'# Results: {results.count()}')

        if show_results:
            for result in results.limit(RESULT_LIMIT).all():
                print(result)
                print(result._email_addresses)

        print('------------------')
