def clean_name(name):
    """Cleans names, ex. for contacts"""
    if not name or name is '':
        return None
    if name[0] in ["'", '"']:
        name = name[1:]
    if name[-1] in ["'", '"']:
        name = name[:-1]
    return name
