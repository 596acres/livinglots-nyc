# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0005_lotlayer'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='owner_opt_in',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
