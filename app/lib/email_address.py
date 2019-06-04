from email.utils import parseaddr


def valid_email(email_str):
    """Returns a valid email address or False"""
    ea = parseaddr(email_str)[1]
    if not ea or ea == '' or '@' not in ea or '.' not in ea or not ea.split('@')[0]:
        return False
    return ea

def clean_email(email_str):
    """Cleans email addresses.
    Ex. Myra.Gupta@gmail.com is equivalent to myragupta@gmail.com
    """
    address, domain = email_str.split('@')
    address = address.replace('.', '')
    address = address.lower()
    return f'{address}@{domain}'

# def email_address_table():
#     """Returns a  """


#     class 