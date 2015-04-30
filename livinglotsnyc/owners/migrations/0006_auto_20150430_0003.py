# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0005_auto_20150317_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownercontact',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
