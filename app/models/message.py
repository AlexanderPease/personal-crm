from app.models import db


class Message(db.Model):
    """A single message"""
    id = db.Column(db.Integer, primary_key=True)

    # Many Messages for a single Mailbox
    mailbox_id = db.Column(db.Integer, db.ForeignKey('mailbox.id'))
    mailbox = db.relationship("Mailbox", back_populates="messages")

    # Gmail
    message_id = db.Column(db.String())
    thread_id = db.Column(db.String())

    raw_headers = db.Column(db.JSON())
    # todo delete headers_raw
    headers_raw = db.Column(db.String())

    def __repr__(self):
        return '<Message {}>'.format(self.id)


class EmailAddress(db.Model):
    """A single email address."""
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(), nullable=False)
    name = db.Column(db.String())

    # Contact
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship("Contact", back_populates="email_addresses")

    def __repr__(self):
        return self.email_address


class MessageEmailAddress(db.Model):
    """For connecting Messages to EmailAddress tables."""
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, nullable=False)
    email_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(), nullable=False)  # Ex. To, Bcc
