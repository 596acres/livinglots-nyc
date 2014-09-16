from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms.module.medialibrary.fields import ContentWithMediaFile
from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent

from livinglots_pathways.cms import PathwayListContent

from pathways.models import Pathway


class CollapsibleSectionContent(RichTextContent):

    title = models.CharField(_('title'), max_length=200)
    start_collapsed = models.BooleanField(_('start collapsed'), default=False)

    class Meta:
        abstract = True
        verbose_name = _('collapsible section')
        verbose_name_plural = _('collapsible sections')

    def render(self, **kwargs):
        return render_to_string('cms/collapsiblesection/default.html',
            { 'content': self }, context_instance=kwargs.get('context'))


class RecentActivitiesContent(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('recent activity list')
        verbose_name_plural = _('recent activity lists')

    def render(self, **kwargs):
        return render_to_string([
            'activity/plugin.html',
        ], {}, context_instance=kwargs.get('context'))


class ExternallyLinkedMediaFileContent(ContentWithMediaFile):

    class Meta:
        abstract = True
        verbose_name = _('externally linked media file')
        verbose_name_plural = _('externally linked media files')

    @classmethod
    def initialize_type(cls):
        cls.add_to_class('external_url', models.URLField(_('external url'),
                                                         blank=True, null=True))

    def render(self, **kwargs):
        ctx = { 'content': self }
        ctx.update(kwargs)
        return render_to_string([
            'content/externallylinkedmediafile/%s.html' % self.mediafile.type,
            'content/externallylinkedmediafile/default.html',
        ], ctx, context_instance=kwargs.get('context'))


class MailchimpSignup(models.Model):

    header_text = models.CharField(_('header text'),
        max_length=50,
    )

    button_text = models.CharField(_('button text'),
        max_length=50,
    )

    user_id = models.CharField(_('Mailchimp user id'),
        max_length=50,
        help_text=_('Provided when generating an embed code (u parameter)'),
    )

    list_id = models.CharField(_('Mailchimp list id'),
        max_length=50,
        help_text=_('Provided under List > Settings > Unique id'),
    )

    class Meta:
        abstract = True
        verbose_name = _('Mailchimp signup')
        verbose_name_plural = _('Mailchimp signup')

    def render(self, **kwargs):
        ctx = { 'signup': self }
        ctx.update(kwargs)
        return render_to_string([
            'content/mailchimp/signup.html',
        ], ctx, context_instance=kwargs.get('context'))


Page.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',

    'pagepermissions.extension',
)

Page.register_templates({
    'title': _('Standard template'),
    'path': 'base.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ('footer_main', _('Footer Main'), 'inherited'),
        ('footer_left', _('Footer Left'), 'inherited'),
        ('footer_right', _('Footer Right'), 'inherited'),
        ('footer_bottom', _('Footer Bottom'), 'inherited'),
    ),
})

Page.register_templates({
    'title': _('Map template'),
    'path': 'map.html',
    'regions': (
        ('main', _('Main content area')),
        ('welcome', _('Welcome text')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ('footer_main', _('Footer Main'), 'inherited'),
        ('footer_left', _('Footer Left'), 'inherited'),
        ('footer_right', _('Footer Right'), 'inherited'),
        ('footer_bottom', _('Footer Bottom'), 'inherited'),
    ),
})

Page.create_content_type(RichTextContent)

Page.create_content_type(CollapsibleSectionContent)
Page.create_content_type(PathwayListContent)
Page.create_content_type(RecentActivitiesContent)

Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))

Page.create_content_type(ExternallyLinkedMediaFileContent)
Page.create_content_type(MailchimpSignup)

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('livinglots_lots.map_urls', _('Lots map')),
    ('elephantblog.urls', _('Blog')),
    ('extraadmin.cms_urls', _('Extra admin functions')),
    ('contact_form', _('Contact form'), {
        'urls': 'contact.form_urls',
    }),
    ('pathways.urls', _('Pathways')),
))


Pathway.register_extensions(
    'feincms.module.extensions.translations',
)

Pathway.register_regions(
    ('main', _('Main content area')),
)

Pathway.create_content_type(RichTextContent)

Pathway.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
))
