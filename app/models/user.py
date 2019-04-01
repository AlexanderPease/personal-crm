from flask_login import UserMixin

from app.models import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Google Auth is only supported method, currently
    email = db.Column(db.String(), nullable=False)
    google_credentials = db.Column(db.JSON())

    # User has many Mailboxes, which each have many Messages
    mailboxes = db.relationship(
        "Mailboxes", back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.email)
