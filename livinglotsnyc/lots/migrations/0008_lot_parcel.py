# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0001_initial'),
        ('lots', '0007_auto_20140927_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='parcel',
            field=models.ForeignKey(related_name=b'lotmodel', blank=True, to='parcels.Parcel', null=True),
            preserve_default=True,
        ),
    ]
