EMAIL_STATUS_NORMAL = 0
EMAIL_STATUS_IGNORE = 1


# SQL substrings for ignoring email addresses
BLACKLIST_EMAIL_SUBSTRINGS = [
    '%newsletter%',
    '%%info%',
    '%%support%',
    '%%notification%',
    '%%mailer%',
    '%%reply%',
    'hello@',
    'team@',

    # Personal
    '%%alexanderpease.com'

    # Redundant with general reply
    # '%%do-not-reply%',
    # '%%donotreply%',
    # '%%do_not_reply%',
    # '%no-reply%',
    # '%noreply%',
]
