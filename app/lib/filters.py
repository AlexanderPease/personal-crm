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
