def get_or_abort(cls, _id):
    obj = cls.query.get(_id)
    if not obj:
        abort(
            404,
            message=f"{cls.__classname__} {_id} doesn't exist"
        )
    return obj