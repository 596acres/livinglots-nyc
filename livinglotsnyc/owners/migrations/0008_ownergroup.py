# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0007_auto_20150430_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('owner_type', models.CharField(default=b'private', max_length=20, verbose_name='owner type', choices=[(b'private', b'private'), (b'public', b'public'), (b'unknown', b'unknown')])),
                ('owners', models.ManyToManyField(to='owners.Owner')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
    ]
