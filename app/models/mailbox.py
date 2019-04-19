from app.models import db


MAILBOX_GMAIL = 'gmail.com'

class Mailbox(db.Model):
    """A single mailbox, ex. joe@gmail.com.
    A User can have multiple mailboxes.

    Relationship to Message: mailbox.messages
    """
    id = db.Column(db.Integer, primary_key=True)

    # TODO: move User.google_credentials to the Mailbox level...
    
    local_part = domain = db.Column(db.String(), nullable=False)
    domain = db.Column(db.String(), nullable=False)

    # TODO this was not populated correctly in /auth
    # A CRM User can have multiple mailboxes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="mailboxes")

    def __init__(self, **kwargs):
        super(Mailbox, self)
        self.domain = MAILBOX_GMAIL

        if 'email_address' in kwargs.keys():
            self.local_part, self.domain = kwargs['email_address'].split('@')

    def __repr__(self):
        return f"Mailbox: {self.email_address}"

    @property
    def email_address(self):
        return f'{self.local_part}@{self.domain}'    
