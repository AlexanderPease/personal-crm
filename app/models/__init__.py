from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()


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
