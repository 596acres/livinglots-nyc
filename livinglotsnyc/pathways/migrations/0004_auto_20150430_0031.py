# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0003_auto_20150324_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathway',
            name='specific_private_owners',
            field=models.ManyToManyField(help_text='This pathway applies to lots with these private owners.', related_name='private+', to='owners.Owner', blank=True),
        ),
        migrations.AlterField(
            model_name='pathway',
            name='specific_public_owners',
            field=models.ManyToManyField(help_text='This pathway applies to lots with these public owners.', related_name='public+', to='owners.Owner', blank=True),
        ),
    ]
