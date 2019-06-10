from sqlalchemy.orm import validates

from app.models import db, ProxyTable
from app.models.mixins.model_mixin import ModelMixin
from app.models.mixins.status_mixin import StatusMixin


class Contact(db.Model, ModelMixin, StatusMixin):
    """A single contact (i.e. a person) may have multiple email addresses.

    Relationship to EmailAddress: contact.email_addresses
        A single Contact can have multiple email addresses.

    Relationship to Tags: contact.tags
        Many-to-many relationship.
    """
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String())
    company = db.Column(db.String())

    def __repr__(self):
        if self.name:
            return self.name
        return f'<Contact: {self.id}>'

    @validates('tags')
    def validate_tags(self, key, tag, include_backrefs=True):
        assert tag.name not in list(map(lambda t: t.name, self.tags))
        return tag


class ContactProxyTable(ProxyTable):
    sql = """
        SELECT
            c.id as "id",
            c.name as "name",
            json_agg(DISTINCT e) as "email_addresses",
            json_agg(DISTINCT t) as "tags",
            COUNT(case when assoc.action = 'from' then 1 ELSE NULL END) as "from_count",
            MAX(case when assoc.action = 'from' then m.datetime else null end) as "from_latest",
            COUNT(case when assoc.action = 'to' or assoc.action = 'cc' or assoc.action = 'bcc' then 1 ELSE NULL END) as "to_count",
            MAX(case when assoc.action = 'to' or assoc.action = 'cc' or assoc.action = 'bcc' then m.datetime ELSE NULL END) as "to_latest"

        FROM contact c

        LEFT JOIN email_address e
        ON e.contact_id = c.id

        LEFT JOIN message_email_address assoc
        ON e.id = assoc.email_id

        LEFT JOIN message m
        on m.id = assoc.message_id

        LEFT JOIN tag_contact assoc_tag
        ON c.id = assoc_tag.contact_id

        LEFT JOIN tag t
        ON t.id = assoc_tag.tag_id

        WHERE e.status = 0

        GROUP BY c.id, c.name, e.email_address, e.name
        """ # noqa
