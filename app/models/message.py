from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import relationship, backref, aliased

from app.models import db, ModelMixin


# Executing basic SQL works, returns Message classes
# query = db.session.query(Message.id, MessageEmailAddress.id).join(MessageEmailAddress, Message.id == MessageEmailAddress.message_id)
# print(query.statement)
# values = query.all()
# print(values)

HEADER_ACTIONS = ['from', 'to', 'cc', 'bcc', 'delivered-to']


class Message(db.Model, ModelMixin):
    """A single message."""
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime(), default=datetime.utcnow)

    # Many Messages for a single Mailbox
    mailbox_id = db.Column(db.Integer, db.ForeignKey('mailbox.id'))
    mailbox = relationship("Mailbox", backref="messages")

    # Gmail
    message_id = db.Column(db.String(), unique=True)
    thread_id = db.Column(db.String())
    # Raw Gmail.Resource dict, includes everything about message
    raw_resource = db.Column(db.JSON())

    datetime = db.Column(db.DateTime(), nullable=True)

    # Is there a way to dynamically create these?
    _email_addresses = relationship(
        "EmailAddress",
        secondary="message_email_address", lazy='dynamic', backref=backref("_messages", lazy='dynamic'))
    _email_addresses_from = relationship(
        "EmailAddress",
        primaryjoin="and_(Message.id==MessageEmailAddress.message_id, MessageEmailAddress.action=='from')",
        secondary="message_email_address",
        lazy='dynamic',
        backref=backref('_messages_from', lazy='dynamic')
    )
    _email_addresses_to = relationship(
        "EmailAddress",
        primaryjoin="and_(Message.id==MessageEmailAddress.message_id, MessageEmailAddress.action=='to')",
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
        action_prop = '_email_addresses_' + action.replace('-', '_')
        pre_existing = getattr(self, action_prop).filter_by(email_address=email_str).all()
        
        if pre_existing and len(pre_existing):
            return

        # Add new connection
        email_address = EmailAddress.get_or_create(
            email_address=email_str, create_kwargs=dict(name=name))
        a = MessageEmailAddress(message_id=self.id, email_id=email_address.id, action=action)
        db.session.add(a)
        db.session.commit()

        return email_address


################################################################################
# Email Address
################################################################################
class EmailAddress(db.Model, ModelMixin):
    """A single email address.
    
    Relationships to Message: _messages, _messages_from, _messages_to, etc.
    """
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String())

    # Contact - import Contact somewhere in app to use
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = relationship("Contact", backref="email_addresses")

    def __init__(self, email_address, name=None):
        super().__init__()

        # todo: validate email_address format
        self.email_address = email_address.lower()
        self.name = name

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


################################################################################
# Association table
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
