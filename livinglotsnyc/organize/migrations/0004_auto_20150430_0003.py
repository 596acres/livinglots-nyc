# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organize', '0003_auto_20141120_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email', blank=True),
        ),
    ]
