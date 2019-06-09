from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm.exc import NoResultFound


db = SQLAlchemy()
ma = Marshmallow()


class ModelMixin(object):
    """Generic methods useful for models."""

    @classmethod
    def get_or_create(cls, create_kwargs=dict(), **query_kwargs):
        """
        Assumes all kwargs are applicable for both get and create.
        create_kwargs used only when creating a new instance

        Returns None if failed to find AND create.
        """
        try:
            return cls.query.filter_by(**query_kwargs).one()
        except NoResultFound:
            pass

        try:
            kwargs = {**query_kwargs, **create_kwargs}
            obj = cls(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except ValueError:
            return


class ProxyTable(object):
    """Generic class for tables joined by raw SQL.
    Enables complex, performant joins."""

    sql = None
    col_mapping = {}

    def __init__(self, **kwargs):
        self.data = db.session.execute(self.sql)

    def __iter__(self):
        for d in self.data:
            yield d

    def get(self, row, name):
        return row[self.col_mapping.get(name, 0)]
