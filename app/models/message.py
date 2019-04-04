from sqlalchemy import and_

from app.models import db


# Join Message and EmailAddress tables
aux_message_email_address = db.Table('message_email_address',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id'), nullable=False),
    db.Column('email_id', db.Integer, db.ForeignKey('email_address.id'), nullable=False),
    db.Column('action', db.String(), nullable=False)  # Ex. From, To, Bcc
)


class Message(db.Model):
    """A single message."""
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

    # todo delete header_from_id
    header_from_id = db.Column(db.Integer, db.ForeignKey('message_email_address.id'))
    
    # Not sure why this didn't work
    # header_from = db.relationship(
    #     "EmailAddress",
    #     # uselist=False,
    #     secondary=aux_message_email_address,
    #     primaryjoin=and_(id==aux_message_email_address.c.message_id, aux_message_email_address.c.action=='from'),
    #     secondaryjoin=(id==aux_message_email_address.c.email_id)
    # )

    # todo delete header_to_id
    header_to_id = db.Column(db.Integer, db.ForeignKey('message_email_address.id'))
    # header_to = db.relationship("MessageEmailAddress", back_populates='message_id')

    def __repr__(self):
        return '<Message {}>'.format(self.id)

    @property
    def from_email(self):
        return self._from_email[0]


class EmailAddress(db.Model):
    """A single email address."""
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String())

    messages_from = db.relationship(
        "Message",
        secondary=aux_message_email_address,
        primaryjoin=and_(id==aux_message_email_address.c.email_id, aux_message_email_address.c.action=='from'),
        secondaryjoin=(Message.id==aux_message_email_address.c.message_id),
        backref="_from_email"
    )

    messages_to = db.relationship(
        "Message",
        secondary=aux_message_email_address,
        primaryjoin=and_(id==aux_message_email_address.c.email_id, aux_message_email_address.c.action=='to'),
        secondaryjoin=(Message.id==aux_message_email_address.c.message_id),
        backref="_to_emails"
    )

    # Contact - not yet in use
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship("Contact", back_populates="email_addresses")

    def __init__(self, **kwargs):
        super(EmailAddress, self)

        if 'email_address' in kwargs.keys():
            self.email_address = kwargs['email_address'].lower()

    def __repr__(self):
        return self.email_address    
