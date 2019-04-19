from flask_restful import abort

def get_or_abort(cls, _id):
    obj = cls.query.get(_id)
    if not obj:
        abort(404, message=f"{cls.__name__} {_id} doesn't exist")
    return obj