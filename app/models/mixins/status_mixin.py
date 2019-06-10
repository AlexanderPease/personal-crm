from app.models import db
from sqlalchemy_utils import ChoiceType


OBJECT_STATUS_ACTIVE = 'a'
OBJECT_STATUS_DELETED = 'd'

OBJECT_STATUS = [
    (OBJECT_STATUS_ACTIVE, 'Active'),
    (OBJECT_STATUS_DELETED, 'Deleted')
]


class StatusMixin(object):
    # Safe deletion of objects
    obj_status = db.Column(
        ChoiceType(OBJECT_STATUS),
        default=OBJECT_STATUS_ACTIVE
    )
