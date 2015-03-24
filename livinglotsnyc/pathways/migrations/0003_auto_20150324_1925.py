# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0002_pathway_borough'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pathway',
            options={'ordering': ('order', 'name')},
        ),
        migrations.AddField(
            model_name='pathway',
            name='order',
            field=models.PositiveIntegerField(default=10),
            preserve_default=True,
        ),
    ]
