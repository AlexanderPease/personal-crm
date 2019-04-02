from app.models import db


class Message(db.Model):
    """A single message"""
    id = db.Column(db.Integer, primary_key=True)

    # Many Messages for a single Mailbox
    mailbox_id = db.Column(db.Integer, db.ForeignKey('mailbox.id'))
    mailbox = db.relationship("Mailbox", back_populates="messages")

    # Gmail
    message_id = db.Column(db.String(), unique=True)
    thread_id = db.Column(db.String())
    # Raw Gmail.Resource dict, includes everything about message
    raw_resource = db.Column(db.JSON())

    # todo delete raw_headers
    raw_headers = db.Column(db.JSON())
    # todo delete headers_raw
    headers_raw = db.Column(db.String())

    header_from_id = db.Column(db.Integer, db.ForeignKey('message_email_address.id'))
    header_from = db.relationship(
        "MessageEmailAddress",
        uselist=False,
        primaryjoin="and_(Message.id==MessageEmailAddress.message_id, "
                    "MessageEmailAddress.action=='from')"
        )
        # secondaryjoin="MessageEmailAddress.email_id==EmailAddress.id",
        # secondary=EmailAddress.__table__)

    header_to_id = db.Column(db.Integer, db.ForeignKey('message_email_address.id'))
    # header_to = db.relationship("MessageEmailAddress", back_populates='message_id')

    def __repr__(self):
        return '<Message {}>'.format(self.id)


class EmailAddress(db.Model):
    """A single email address."""
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String())

    # Contact - not yet in use
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship("Contact", back_populates="email_addresses")

    def __init__(self, **kwargs):
        super(EmailAddress, self)

        if 'email_address' in kwargs.keys():
            self.email_address = kwargs['email_address'].lower()

    def __repr__(self):
        return self.email_address


class MessageEmailAddress(db.Model):
    """For connecting Messages to EmailAddress tables."""
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    
    email_id = db.Column(db.Integer, db.ForeignKey('email_address.id'), nullable=False)
    email_address = db.relationship("EmailAddress",uselist=False)
    
    action = db.Column(db.String(), nullable=False)  # Ex. From, To, Bcc
