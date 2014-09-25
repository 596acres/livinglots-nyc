# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0002_ownercontact'),
        ('lots', '0003_auto_20140924_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='owner_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='owners.OwnerContact', help_text='The owner of this lot.', null=True, verbose_name='owner'),
            preserve_default=True,
        ),
    ]
