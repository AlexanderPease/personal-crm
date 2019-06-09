from email.utils import parseaddr


def valid_email(email_str):
    """Returns a valid email address or False"""
    ea = parseaddr(email_str)[1]
    if not ea or ea == '' or '@' not in ea or '.' not in ea or not ea.split('@')[0]:
        return False
    return ea


def clean_email(email_str):
    """Cleans email addresses.
    Ex. Myra.Gupta@gmail.com is equivalent to myra.gupta@gmail.com
    """
    address, domain = email_str.split('@')
    address = address.lower()
    return f'{address}@{domain}'


def generate_name(email_str):
    """Given an email address, guess the name.
    Useful when a name is not given."""
    name = email_str.split('@')[0]
    name = name.replace('.', ' ').replace('_', ' ')
    for num in range(0, 10):
        name = name.replace(str(num), '')
    name = name.title()
    return name
