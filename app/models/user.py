from flask_login import UserMixin

from app.models import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    google_credentials = db.Column(db.JSON())

    # User has many Mailboxes, which each have many Messages
    mailboxes = db.relationship(
        "Mailboxes", back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.email)
