# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0011_auto_20141024_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='gutterspace',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
