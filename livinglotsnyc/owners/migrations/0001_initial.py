# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinglots_owners', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256, verbose_name='name')),
                ('owner_type', models.CharField(default=b'private', max_length=20, verbose_name='owner type', choices=[(b'private', b'private'), (b'public', b'public'), (b'unknown', b'unknown')])),
                ('aliases', models.ManyToManyField(help_text='Other names for this owner', to='livinglots_owners.Alias', null=True, verbose_name='aliases', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
