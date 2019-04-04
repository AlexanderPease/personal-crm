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

    @property
    def email_address(self, **kwargs):
        """All EmailAddress objects in the headers of this message."""
        return self.__query_email_addresses()

    @property
    def from_email_address(self):
        """Returns the single EmailAddress in From: header."""
        return self.__query_email_addresses(action='from')[0]

    @property
    def to_email_address(self):
        """Returns all EmailAddress objects in To: header."""
        return self.__query_email_addresses(action='to')

    def __query_email_addresses(self, **kwargs):
        return [assoc.email_address for assoc in self._email_addresses.filter_by(**kwargs).all()]
    

    def add_email_address(self, email_str, action):
        """Setter method for all related EmailAddress objects.

        Args:
            email_str: A string, ex. "david@gmail.com"
            action: A string describing header action, ex. "from"

        """
        if action not in HEADER_ACTIONS:
            print(f'Attempted to add malformed action {action} to {self}')
            return

        # Ensure only a single unique connection between Message and EmailAddress
        # for a given action, ex. To:
        pre_existing = self.__query_email_addresses(
            email_address=email_str,
            action=action)
        if pre_existing:
            return

        # Add new connection
        a = MessageEmailAddress(action=action)
        a.email_address = EmailAddress.get_or_create(email_address=email_address)
        self._email_addresses.append(a)
        db.session.add(self)
        db.session.commit()

        # # Add new connection
        # try:
        #     new = MessageEmailAddress(
        #         email_id=email_address.id,
        #         message_id=self.id,
        #         action=action
        #     )
        #     db.session.add(new)
        #     db.session.commit()
        # except:
        #     print('Failure to add MessageEmailAddress')


class EmailAddress(db.Model):
    """A single email address."""
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String())

    _messages = relationship("MessageEmailAddress", lazy='dynamic', backref=backref("email_address"))
    # message = relationship("Message", secondary="message_email_address")


    #     messages_from = relationship(
    #     "Message",
    #     secondary=aux_message_email_address,
    #     primaryjoin=and_(id==aux_message_email_address.c.email_id, aux_message_email_address.c.action=='from'),
    #     secondaryjoin=(Message.id==aux_message_email_address.c.message_id),
    #     backref="_from_email"
    # )
    # messages_from = relationship(
    #     "Message",
    #     secondary="MessageEmailAddress",
    #     primaryjoin=and_(id==MessageEmailAddress.email_id, MessageEmailAddress.action=='from'),
    #     secondaryjoin=(Message.id==Message.message_id),
    #     backref="_from_email"
    # )

    

    # messages_to = relationship(
    #     "Message",
    #     secondary=aux_message_email_address,
    #     primaryjoin=and_(id==aux_message_email_address.c.email_id, aux_message_email_address.c.action=='to'),
    #     secondaryjoin=(Message.id==aux_message_email_address.c.message_id),
    #     backref="to_emails"
    # )

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
    def get_or_create(cls, email_str):
        try:
            return EmailAddress.query.filter_by(
                email_address=email_str).one()
        except NoResultFound:
            email_address = EmailAddress(email_address=email_str)
            db.session.add(email_address)
            db.session.commit()
            return email_address


# Join Message and EmailAddress tables
class MessageEmailAddress(db.Model):
    # __tablename__ = 'message_email_address'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey('email_address.id'), nullable=False)
    action = db.Column(db.String(), nullable=False)  # Ex. From, To, Bcc

    # message = relationship("Message", back_populates="_email_addresses", lazy='dynamic')
    # email_address = relationship("EmailAddress", back_populates="_messages", lazy='dynamic')

    # message = relationship(Message, backref=backref("message_email_address", cascade="all, delete-orphan"))
    # email_address = relationship(EmailAddress, backref=backref("message_email_address", cascade="all, delete-orphan"))

# association_table = aliased(MessageEmailAddress)