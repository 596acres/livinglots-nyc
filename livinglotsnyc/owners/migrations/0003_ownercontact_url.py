# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0002_ownercontact'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownercontact',
            name='url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
