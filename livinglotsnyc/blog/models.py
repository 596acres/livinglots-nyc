from django.utils.translation import ugettext_lazy as _

from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
import feincms_cleanse

from elephantblog.models import Entry


Entry.register_extensions(
    'feincms.module.extensions.translations',
    'feincms.module.extensions.datepublisher',
)

Entry.register_regions(
    ('main', _('Main content area')),
    ('teaser', _('Blog entry teaser')),
)

Entry.create_content_type(
    RichTextContent,
    cleanse=feincms_cleanse.cleanse_html,
    regions=('main', 'teaser',)
)

Entry.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
