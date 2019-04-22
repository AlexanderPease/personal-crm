from app.models import db, ModelMixin


class Contact(db.Model, ModelMixin):
    """A single contact (i.e. a person) may have multiple email addresses.

    Relationship to EmailAddress: email_addresses
    """
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String())
    company = db.Column(db.String())

    def __repr__(self):
        if self.name:
            return self.name
        return f'<Contact: {self.id}>'
