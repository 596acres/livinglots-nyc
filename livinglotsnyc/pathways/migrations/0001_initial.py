# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.extensions
import livinglots_pathways.cms
import feincms.contrib.richtext
from django.conf import settings
import caching.base
import feincms.module.medialibrary.fields


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0004_owner_default_contact'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medialibrary', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFileContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('type', models.CharField(default=b'default', max_length=20, verbose_name='type', choices=[(b'default', 'default')])),
                ('mediafile', feincms.module.medialibrary.fields.MediaFileForeignKey(related_name='+', verbose_name='media file', to='medialibrary.MediaFile')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'media files',
                'db_table': 'pathways_pathway_mediafilecontent',
                'verbose_name': 'media file',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pathway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('slug', models.SlugField(max_length=256, verbose_name='slug')),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='is active')),
                ('private_owners', models.BooleanField(default=False, help_text='This pathway applies to lots with private owners.', verbose_name='private owners')),
                ('public_owners', models.BooleanField(default=False, help_text='This pathway applies to lots with public owners.', verbose_name='public owners')),
                ('language', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'English'), (b'es', b'Spanish')])),
                ('author', models.ForeignKey(verbose_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('specific_private_owners', models.ManyToManyField(help_text='This pathway applies to lots with these private owners.', related_name='private+', null=True, to='owners.Owner', blank=True)),
                ('specific_public_owners', models.ManyToManyField(help_text='This pathway applies to lots with these public owners.', related_name='public+', null=True, to='owners.Owner', blank=True)),
                ('translation_of', models.ForeignKey(related_name='translations', blank=True, to='pathways.Pathway', help_text='Leave this empty for entries in the primary language.', null=True, verbose_name='translation of')),
            ],
            options={
                'abstract': False,
            },
            bases=(caching.base.CachingMixin, livinglots_pathways.cms.PathwayFeinCMSMixin, models.Model, feincms.extensions.ExtensionsMixin),
        ),
        migrations.CreateModel(
            name='RichTextContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', feincms.contrib.richtext.RichTextField(verbose_name='text', blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='richtextcontent_set', to='pathways.Pathway')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'rich texts',
                'db_table': 'pathways_pathway_richtextcontent',
                'verbose_name': 'rich text',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mediafilecontent',
            name='parent',
            field=models.ForeignKey(related_name='mediafilecontent_set', to='pathways.Pathway'),
            preserve_default=True,
        ),
    ]
