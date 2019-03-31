from app.models import db


class Contact(db.Model):
    """A single contact (i.e. a person) has multiple email addresses."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email_addresses = db.relationship(
        "Email Addresses", back_populates="contact")
