from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm.exc import NoResultFound


db = SQLAlchemy()
ma = Marshmallow()


class ModelMixin(object):
    """Generic methods useful for models."""

    @classmethod
    def get_or_create(cls, create=dict(), **kwargs):
        """
        Assumes all kwargs are applicable for both get and create
        Uses create dictionary only when creating a new instance.  
        """
        try:
            return cls.query.filter_by(**kwargs).one()
        except NoResultFound:
            obj = cls(**create, **kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj