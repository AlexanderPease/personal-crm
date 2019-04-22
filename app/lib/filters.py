from flask import Blueprint

filters = Blueprint('filters', __name__)


@filters.app_template_filter('date')
def format_date(dt):
    if dt:
        return dt.strftime('%Y/%m/%d')


@filters.app_template_filter('empty')
def empty(string):
    if not string or string == 'None':
        return ''
    return string


@filters.app_template_filter('list_to_string')
def list_to_string(_list,  attr=None, func=str, delimit=', '):
    value = ''
    for obj in _list:
        if attr:
            value += getattr(obj, attr)
        else:
            value += func(obj)
        value += delimit
    return value[:-len(delimit)]
