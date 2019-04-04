from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship, backref, aliased

from app.models import db


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
    mailbox = relationship("Mailbox", back_populates="messages")

    # Gmail
    message_id = db.Column(db.String(), unique=True)
    thread_id = db.Column(db.String())
    # Raw Gmail.Resource dict, includes everything about message
    raw_resource = db.Column(db.JSON())

    _email_addresses = relationship("MessageEmailAddress", lazy='dynamic', backref=backref("message"))
    
    # Not sure why this didn't work
    # header_from = relationship(
    #     "EmailAddress",
    #     # uselist=False,
    #     secondary=aux_message_email_address,
    #     primaryjoin=and_(id==aux_message_email_address.c.message_id, aux_message_email_address.c.action=='from'),
    #     secondaryjoin=(id==aux_message_email_address.c.email_id)
    # )




    def __repr__(self):
        return '<Message {}>'.format(self.id)

    def email_addresses(self, action=None, **kwargs):
        """All EmailAddress objects in the headers of this message."""
        if action and action not in HEADER_ACTIONS:
            return
        
        return self._query_email_addresses(action=action, **kwargs)

    @property
    def from_email_address(self):
        """Returns the single EmailAddress in From: header."""
        try:
            return self._query_email_addresses(action='from')[0]
        except:
            pass

    def _query_email_addresses(self, **kwargs):
        """Can only query on columns in MessageEmailAddress."""
        return [assoc.email_address for assoc in self._email_addresses.filter_by(**kwargs).all()]
    

    def add_email_address(self, email_str, action, name=None):
        """Setter method for all related EmailAddress objects.

        Args:
            email_str: A string, ex. "david@gmail.com"
            action: A string describing header action, ex. "from"
            name: Optional string for name of EmailAddress

        """
        if email_str=='godfred@hansen-nord.dk':
            print(f'{email_str}')
            print(f'{action}')
            print(f'{name}')

        if action not in HEADER_ACTIONS:
            print(f'Attempted to add malformed action {action} to {self}')
            return

        # Ensure connection between Message, EmailAddress, and action is unique
        email_address = EmailAddress.get_or_create(email_str, name)
        kwargs = dict(email_id=email_address.id, action=action)
        pre_existing = self._query_email_addresses(**kwargs)
        if email_str=='godfred@hansen-nord.dk':
            print(f'Preexisting relationship: {pre_existing}')
        if pre_existing and len(pre_existing):
            return

        # Add new connection
        a = MessageEmailAddress(**kwargs)
        self._email_addresses.append(a)
        db.session.add(self)
        db.session.commit()


class EmailAddress(db.Model):
    """A single email address."""
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String())

    _messages = relationship("MessageEmailAddress", lazy='dynamic', backref=backref("email_address"))

    # Contact - not yet in use
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = relationship("Contact", back_populates="email_addresses")

    def __init__(self, **kwargs):
        super(EmailAddress, self)

        if 'email_address' in kwargs.keys():
            self.email_address = kwargs['email_address'].lower()

    def __repr__(self):
        return f'<EmailAddress: {self.email_address}>'

    @classmethod
    def get_or_create(cls, email_str, name_str):
        try:
            return EmailAddress.query.filter_by(
                email_address=email_str).one()
        except NoResultFound:
            email_address = EmailAddress(email_address=email_str, name=name_str)
            db.session.add(email_address)
            db.session.commit()
            return email_address



class MessageEmailAddress(db.Model):    
    # Join Message and EmailAddress tables
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey('email_address.id'), nullable=False)
    action = db.Column(db.String(), nullable=False)  # Ex. From, To, Bcc
