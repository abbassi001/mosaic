from django import template
from number2words import *

register = template.Library()

@register.simple_tag
def number_to_words(value):
    try:
        words = number2words(value, lang='en')
        return words
    except ValueError:
        return value