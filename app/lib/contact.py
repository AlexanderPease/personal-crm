from app.models.mixins.status_mixin import OBJECT_STATUS_DELETED
from app.models import db


def merge_contacts(c1, c2):
    """Merges Contact objects by shifting c2 data into c1.
    Marks c2 as deleted.

    Returns c1 (i.e. the merged contact).
    """
    print(f'Merging {c2.id} into {c1.id}')
    if OBJECT_STATUS_DELETED in [c1.obj_status, c2.obj_status]:
        raise AssertionError

    if not c1.name and c2.name:
        c1.name = c2.name

    for ea in c2.email_addresses:
        ea.contact = c1
        db.session.add(ea)

    for tag in c2.tags:
        try:
            c1.tags.append(tag)
        except AssertionError:
            pass

    c2.obj_status = OBJECT_STATUS_DELETED

    db.session.add_all([c1, c2])
    db.session.commit()

    return c1
