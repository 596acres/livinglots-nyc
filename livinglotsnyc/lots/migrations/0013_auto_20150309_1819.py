# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0012_lot_gutterspace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='bbl',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
