from django import template

import bleach
from bleach.callbacks import nofollow, target_blank
from html5lib.tokenizer import HTMLTokenizer


register = template.Library()


@register.filter(is_safe=True)
def linkify(value):
    return bleach.linkify(value, [nofollow, target_blank,], parse_email=True,
                          tokenizer=HTMLTokenizer)
