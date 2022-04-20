import re
from django import template

register = template.Library()

CENSOR_WORDS = ['nintendo', 'bitcoin']


@register.filter()
def format_date(value):
    return value.strftime("%d.%m.%Y")


@register.filter()
def censor(text):
    if type(text) != str:
        return "Type error. Is not string"

    for word in CENSOR_WORDS:
        text = re.sub(r'(?:'+word[1:]+'?)[^\s]+',
                      ("*" * (len(word) - 1)), text)
    return text
