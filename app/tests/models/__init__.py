from app.models import db
from app.tests import TestBase

class TestModelBase(TestBase):
    """Requires self.model to be set."""
    model = None

    def add(self, **kwargs):
        obj = self.model(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj
