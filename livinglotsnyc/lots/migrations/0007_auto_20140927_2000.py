# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0006_lot_owner_opt_in'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lot',
            old_name='lot',
            new_name='lot_number',
        ),
        migrations.AlterField(
            model_name='lot',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='group', blank=True, to='lots.LotGroup', null=True),
        ),
    ]
