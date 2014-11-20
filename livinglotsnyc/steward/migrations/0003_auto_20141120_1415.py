# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('steward', '0002_stewardproject_started_here'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stewardnotification',
            name='email',
            field=models.EmailField(max_length=75, null=True, verbose_name='email', blank=True),
            preserve_default=True,
        ),
    ]
