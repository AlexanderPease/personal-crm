from email.utils import parseaddr


def valid_email(email_str):
    """Returns a valid email address or False"""
    ea = parseaddr(email_str)[1]
    if not ea or ea == '' or '@' not in ea or '.' not in ea or not ea.split('@')[0]:
        return False
    return ea