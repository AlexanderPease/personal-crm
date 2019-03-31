from app.models import db


class Message(db.Model):
    """A single message"""
    id = db.Column(db.Integer, primary_key=True)

    # Many Messages for a single Mailbox
    mailbox_id = db.Column(db.Integer, db.ForeignKey('mailbox.id'))
    mailbox = db.relationship("User", back_populates="messages")

    # Gmail
    message_id = db.Column(db.String())
    thread_id = db.Column(db.String())

    headers_raw = db.Column(db.String())

    def __repr__(self):
        return '<Message {}>'.format(self.id)


class EmailAddress(db.Model):
    """A single email address."""
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(), required=True)
    name = db.Column(db.String())

    # Contact
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship("Contact", back_populates="email_addresses")

    def __repr__(self):
        return self.email_address


class MessageEmailAddress(db.Model):
    """For connecting Messages to EmailAddress tables."""
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, required=True)
    email_id = db.Column(db.Integer, required=True)
    action = db.Column(db.String(), required=True)  # Ex. To, Bcc
