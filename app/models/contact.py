from app.models import db, ModelMixin


class Contact(db.Model, ModelMixin):
    """A single contact (i.e. a person) has multiple email addresses.

    Relationship to EmailAddress: email_addresses
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

