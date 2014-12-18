from collections import OrderedDict

from django import template
from django.contrib.contenttypes.models import ContentType

from articles.models import Article
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from taggit.models import Tag, TaggedItem


register = template.Library()


def _faq_tags():
    content_type = ContentType.objects.get_for_model(Article)
    return Tag.objects.filter(
        taggit_taggeditem_items=TaggedItem.objects.filter(content_type=content_type)
    ).order_by('name')


class FaqTags(AsTag):
    """Get tags only pertaining to FAQs"""
    options = Options(
        'as',
        Argument('varname', resolve=False, required=True),
    )

    def get_value(self, context):
        return _faq_tags()


class FaqsTagGroups(AsTag):
    """Get FAQs by tag"""
    options = Options(
        'as',
        Argument('varname', resolve=False, required=True),
    )

    def get_value(self, context):
        groups = OrderedDict()
        for tag in _faq_tags():
            groups[tag] = Article.objects.filter(tags=tag)
        return groups


register.tag(FaqTags)
register.tag(FaqsTagGroups)
