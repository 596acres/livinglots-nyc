# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0003_ownercontact_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='default_contact',
            field=models.ForeignKey(related_name=b'+', blank=True, to='owners.OwnerContact', null=True),
            preserve_default=True,
        ),
    ]
