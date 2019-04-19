# For convenience defining schema
MESSAGE_SIMPLE_SCHEMA = dict(
    only=('id', 'message_id', 'thread_id'),
    many=True
)


EMAIL_SIMPLE_SCHEMA_ONLY = only=('id', 'name', 'email_address')


EMAIL_SIMPLE_SCHEMA = dict(
    only=EMAIL_SIMPLE_SCHEMA_ONLY,
    many=True
)