from app.models import db


class Mailbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())  # Ex. Personal Gmail

    # Mailbox has many messages
    messages = db.relationship(
        "Messages", back_populates="user")

    # A CRM User can have multiple mailboxes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="mailboxes")

    def __repr__(self):
        return self.name
