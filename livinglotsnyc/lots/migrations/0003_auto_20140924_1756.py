# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0002_auto_20140924_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='bbl',
            field=models.CharField(unique=True, max_length=10),
        ),
    ]
