# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathway',
            name='borough',
            field=models.CharField(blank=True, max_length=25, null=True, choices=[(b'Bronx', b'Bronx'), (b'Brooklyn', b'Brooklyn'), (b'Manhattan', b'Manhattan'), (b'Queens', b'Queens'), (b'Staten Island', b'Staten Island')]),
            preserve_default=True,
        ),
    ]
