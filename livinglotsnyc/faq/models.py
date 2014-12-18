from django.utils.translation import ugettext_lazy as _

from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.video.models import VideoContent

from articles.models import Article


Article.register_regions(
    ('question', _('Question')),
    ('answer', _('Answer')),
)

Article.register_extensions(
    'articles.extensions.tags',
)

Article.create_content_type(RichTextContent)
Article.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
Article.create_content_type(VideoContent)
