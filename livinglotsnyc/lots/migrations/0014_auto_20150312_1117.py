# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0013_auto_20150309_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='added_reason',
            field=models.CharField(help_text=b'The original reason this lot was added', max_length=256, null=True, verbose_name='reason added', blank=True),
            preserve_default=True,
        ),
    ]
