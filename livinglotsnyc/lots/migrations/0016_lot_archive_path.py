# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0015_auto_20150317_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='archive_path',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
