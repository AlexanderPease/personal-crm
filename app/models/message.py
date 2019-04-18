from marshmallow import Schema, fields, pre_load, validate
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship, backref, aliased

from app.models import db, ma


# Executing basic SQL works, returns Message classes
# query = db.session.query(Message.id, MessageEmailAddress.id).join(MessageEmailAddress, Message.id == MessageEmailAddress.message_id)
# print(query.statement)
# values = query.all()
# print(values)

HEADER_ACTIONS = ['from', 'to', 'cc', 'bcc', 'delivered-to']


class Message(db.Model):
    """A single message."""
    id = db.Column(db.Integer, primary_key=True)

    # Many Messages for a single Mailbox
    mailbox_id = db.Column(db.Integer, db.ForeignKey('mailbox.id'))
    # mailbox = relationship("Mailbox", backref="messages")

    # Gmail
    message_id = db.Column(db.String(), unique=True)
    thread_id = db.Column(db.String())
    # Raw Gmail.Resource dict, includes everything about message
    raw_resource = db.Column(db.JSON())

    # Is there a way to dynamically create these?
    _email_addresses = relationship(
        "EmailAddress",
        secondary="message_email_address", lazy='dynamic', backref=backref("_messages", lazy='dynamic'))
    _email_addresses_from = relationship(
        "EmailAddress",
        primaryjoin="and_(Message.id==MessageEmailAddress.message_id, MessageEmailAddress.action=='to')",
        secondary="message_email_address",
        lazy='dynamic',
        backref=backref('_messages_from', lazy='dynamic')
    )
    _email_addresses_to = relationship(
        "EmailAddress",
        primaryjoin="and_(Message.id==MessageEmailAddress.message_id, MessageEmailAddress.action=='from')",
        secondary="message_email_address",
        lazy='dynamic',
        backref=backref('_messages_to', lazy='dynamic')
    )
    _email_addresses_cc = relationship(
        "EmailAddress",
        primaryjoin="and_(Message.id==MessageEmailAddress.message_id, MessageEmailAddress.action=='cc')",
        secondary="message_email_address",
        lazy='dynamic',
        backref=backref('_messages_cc', lazy='dynamic')
    )
    _email_addresses_bcc = relationship(
        "EmailAddress",
        primaryjoin="and_(Message.id==MessageEmailAddress.message_id, MessageEmailAddress.action=='bcc')",
        secondary="message_email_address",
        lazy='dynamic',
        backref=backref('_messages_bcc', lazy='dynamic')
    )
    _email_addresses_delivered_to = relationship(
        "EmailAddress",
        primaryjoin="and_(Message.id==MessageEmailAddress.message_id, MessageEmailAddress.action=='delivered-to')",
        secondary="message_email_address",
        lazy='dynamic',
        backref=backref('_messages_delivered_to', lazy='dynamic')
    )

    def __repr__(self):
        return '<Message {}>'.format(self.id)

    def email_addresses(self, action=None, **kwargs):
        """All EmailAddress objects in the headers of this message."""
        if action and action not in HEADER_ACTIONS:
            return
        elif action:
            email_addresses = getattr(self, '_email_addresses_' + action.replace('-', '_'))
        else:
            email_addresses = self._email_addresses

        return email_addresses.filter_by(**kwargs).all()

    @property
    def from_email_address(self):
        """Returns the single EmailAddress in From: header."""
        try:
            return self._email_addresses_from[0]
        except:
            pass

    def add_email_address(self, email_str, action, name=None):
        """Setter method for all related EmailAddress objects.

        Args:
            email_str: A string, ex. "david@gmail.com"
            action: A string describing header action, ex. "from"
            name: Optional string for name of EmailAddress

        """
        if action not in HEADER_ACTIONS:
            print(f'Attempted to add malformed action {action} to {self}')
            return

        # Ensure connection between Message, EmailAddress, and action is unique
        email_address = EmailAddress.get_or_create(email_str, name)
        kwargs = dict(email_id=email_address.id, action=action)
        pre_existing = self._query_email_addresses(**kwargs)
        if pre_existing and len(pre_existing):
            return

        # Add new connection
        a = MessageEmailAddress(**kwargs)
        self._email_addresses.append(a)
        db.session.add(self)
        db.session.commit()


class EmailAddressMessageSchema(ma.Schema):
    id = fields.Integer()
    email_address = fields.String()
    name = fields.String()

# NB: ModelSchema doesn't play nice with relationships
class MessageSchema(ma.Schema):
    id = fields.Integer()
    mailbox = fields.String()
    message_id = fields.String()
    thread_id = fields.String()
    email_addresses = fields.Nested(
        'EmailAddressSchema',
        attribute='email_addresses',
        only=('id', 'name', 'email_address'),
        many=True)


################################################################################
# Email Address
################################################################################
class EmailAddress(db.Model):
    """A single email address."""
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String())

    # Relationships to Message:
    # _messages, _messages_from, _messages_to, etc.

    # Contact - not yet in use
    # contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    # contact = relationship("Contact", back_populates="email_addresses")

    def __init__(self, **kwargs):
        super(EmailAddress, self)

        if 'email_address' in kwargs.keys():
            self.email_address = kwargs['email_address'].lower()

    def __repr__(self):
        return f'<EmailAddress: {self.email_address}>'

    def messages(self, action=None, **kwargs):
        """All Messages objects of header action."""
        if action and action not in HEADER_ACTIONS:
            return
        elif action:
            messages = getattr(self, '_messages_' + action.replace('-', '_'))
        else:
            messages = self._messages

        return messages.filter_by(**kwargs).all()

    @classmethod
    def get_or_create(cls, email_str, name_str):
        try:
            return EmailAddress.query.filter_by(
                email_address=email_str).one()
        except NoResultFound:
            email_address = EmailAddress(
                email_address=email_str,
                name=name_str
            )
            db.session.add(email_address)
            db.session.commit()
            return email_address


class EmailAddressSchema(ma.Schema):
    id = fields.Integer()
    email_address = fields.String()
    name = fields.String()
    messages = fields.String()
    # _messages = fields.Nested("MessageEmailAddressSchema")


################################################################################
# Join table
################################################################################
class MessageEmailAddress(db.Model):
    # Join Message and EmailAddress tables
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(
        db.Integer, db.ForeignKey('message.id'), nullable=False)
    email_id = db.Column(
        db.Integer, db.ForeignKey('email_address.id'), nullable=False)
    action = db.Column(db.String(), nullable=False)  # Ex. From, To, Bcc

    message = db.relationship("Message", backref=backref("message_email_address", lazy='dynamic'))
    email_address = db.relationship("EmailAddress", backref=backref("message_email_address", lazy='dynamic'))
