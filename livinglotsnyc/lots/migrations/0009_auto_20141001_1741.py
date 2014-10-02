# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0008_lot_parcel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='bbl',
            field=models.CharField(max_length=10, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='block',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='lot_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
