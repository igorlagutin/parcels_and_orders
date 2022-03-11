from datetime import datetime, timedelta
from django import template

register = template.Library()


@register.filter
def older_five_days(value):
    if datetime.now().date() - value > timedelta(days=3):
        return True
    else:
        return False
