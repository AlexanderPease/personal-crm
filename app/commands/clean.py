import click
from flask import current_app as app

from app.lib.clean import clean_name
from app.lib.email_address import valid_email
from app.models import db
from app.models.contact import Contact
from app.models.message import EmailAddress, MessageEmailAddress


@app.cli.command('clean-emails')
@click.option('--dry-run', is_flag=True, default=False)
def clean_emails(dry_run):
    """Removes malformed EmailAddresses created prior to validation."""
    emails = EmailAddress.query.all()
    print(f'Retrieved malformed email addresses...')

    for ea in emails:
        if valid_email(ea.email_address):
            continue
        if dry_run:
            print(f'{ea}, ID: {ea.id}, Assoc.: {ea.message_email_address.all()}')
        else:
            db.session.delete(ea)
            db.session.query(MessageEmailAddress).filter(MessageEmailAddress.email_id==ea.id).delete()

    if not dry_run:
        db.session.commit()

    print('Success')



@app.cli.command('clean-contacts')
def clean_contacts():
    """Included in worker.generate_contacts (Step 5)"""
    for contact in Contact.query:
        contact.name = clean_name(contact.name)
        db.session.add(contact)
        db.session.commit()

    print('Success')