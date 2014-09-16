# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinglots_lots', '__first__'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroundtruthRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('actual_use', models.TextField(help_text='How is this actually being used?', verbose_name='actual use')),
                ('contact_name', models.CharField(help_text="What's your name?", max_length=50, verbose_name='contact name')),
                ('contact_email', models.EmailField(help_text='Who can we email for more information?', max_length=75, null=True, verbose_name='contact email', blank=True)),
                ('contact_phone', models.CharField(help_text='Who can we call for more information?', max_length=20, null=True, verbose_name='contact phone', blank=True)),
                ('added', models.DateTimeField(help_text=b'When this record was added', verbose_name='date added', auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('use', models.ForeignKey(verbose_name='use', blank=True, to='livinglots_lots.Use', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
