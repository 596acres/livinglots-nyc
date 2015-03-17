# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0014_auto_20150312_1147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lotgroup',
            options={'ordering': ['name']},
        ),
    ]
