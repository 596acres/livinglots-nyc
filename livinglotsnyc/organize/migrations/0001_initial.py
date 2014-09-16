# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('livinglots_organize', '__first__'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('phone', models.CharField(max_length=32, null=True, verbose_name='phone', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email')),
                ('email_hash', models.CharField(max_length=40, null=True, editable=False, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('url', models.URLField(null=True, verbose_name='url', blank=True)),
                ('notes', models.TextField(null=True, verbose_name='notes', blank=True)),
                ('facebook_page', models.CharField(help_text=b'The Facebook page for your organization. Please do not enter your personal Facebook page.', max_length=256, null=True, verbose_name='facebook page', blank=True)),
                ('post_publicly', models.BooleanField(default=True, help_text="Check this if you want to share your information on the lot's page so that your neighbors can reach you and work for access together. (If you don't click it, we'll just send you updates but keep your information hidden.)", verbose_name='post publicly')),
                ('added_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('type', models.ForeignKey(to='livinglots_organize.OrganizerType')),
            ],
            options={
                'abstract': False,
                'permissions': (('email_organizers', 'Can send an email to all organizers'),),
            },
            bases=(models.Model,),
        ),
    ]
