# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0010_auto_20141023_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='parcel',
            field=models.ForeignKey(blank=True, to='parcels.Parcel', null=True),
            preserve_default=True,
        ),
    ]
