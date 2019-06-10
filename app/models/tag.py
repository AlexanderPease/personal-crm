from sqlalchemy.orm import relationship

from app.models import db
from app.models.mixins.model_mixin import ModelMixin


tag_contact = db.Table(
    'tag_contact',
    db.Column('contact_id', db.ForeignKey('contact.id')),
    db.Column('tag_id', db.ForeignKey('tag.id'))
)


class Tag(db.Model, ModelMixin):
    """Tags for organizing contacts."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    contacts = relationship(
        "Contact",
        secondary=tag_contact,
        backref="tags"
    )
