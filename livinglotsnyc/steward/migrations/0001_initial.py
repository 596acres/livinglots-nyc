# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organize', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('livinglots_organize', '__first__'),
        ('contenttypes', '0001_initial'),
        ('livinglots_lots', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='StewardNotification',
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
                ('project_name', models.CharField(help_text='The name of the project using this lot.', max_length=256, verbose_name='project name')),
                ('support_organization', models.CharField(help_text="What is your project's support organization, if any?", max_length=300, null=True, verbose_name='support organization', blank=True)),
                ('land_tenure_status', models.CharField(default='not sure', help_text='What is the land tenure status for the project? (This will not be shared publicly.)', max_length=50, verbose_name='land tenure status', choices=[(b'owned', 'project owns the land'), (b'licensed', 'project has a license for the land'), (b'lease', 'project has a lease for the land'), (b'access', 'project has access to the land'), (b'not sure', "I'm not sure")])),
                ('include_on_map', models.BooleanField(default=True, help_text='Can we include the project on our map?', verbose_name='include on map')),
                ('added_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('type', models.ForeignKey(to='livinglots_organize.OrganizerType')),
                ('use', models.ForeignKey(verbose_name='use', to='livinglots_lots.Use', help_text='How is the project using the land?')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StewardProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(help_text='The name of the project using this lot.', max_length=256, verbose_name='project name')),
                ('support_organization', models.CharField(help_text="What is your project's support organization, if any?", max_length=300, null=True, verbose_name='support organization', blank=True)),
                ('land_tenure_status', models.CharField(default='not sure', help_text='What is the land tenure status for the project? (This will not be shared publicly.)', max_length=50, verbose_name='land tenure status', choices=[(b'owned', 'project owns the land'), (b'licensed', 'project has a license for the land'), (b'lease', 'project has a lease for the land'), (b'access', 'project has access to the land'), (b'not sure', "I'm not sure")])),
                ('include_on_map', models.BooleanField(default=True, help_text='Can we include the project on our map?', verbose_name='include on map')),
                ('object_id', models.PositiveIntegerField()),
                ('external_id', models.CharField(help_text='The external id for this project, if it is stored in other databases', max_length=100, null=True, verbose_name='external id', blank=True)),
                ('date_started', models.DateField(help_text='When did this project start?', null=True, verbose_name='date started', blank=True)),
                ('content_type', models.ForeignKey(related_name=b'+', to='contenttypes.ContentType')),
                ('organizer', models.ForeignKey(blank=True, to='organize.Organizer', help_text='The organizer associated with this project.', null=True, verbose_name='organizer')),
                ('steward_notification', models.ForeignKey(blank=True, to='steward.StewardNotification', help_text='The notification that led to the creation of this project, if any.', null=True, verbose_name='steward notification')),
                ('use', models.ForeignKey(verbose_name='use', to='livinglots_lots.Use', help_text='How is the project using the land?')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
