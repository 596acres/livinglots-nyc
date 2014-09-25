# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('owner', models.ForeignKey(to='owners.Owner')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
