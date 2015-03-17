# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0004_owner_default_contact'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='owner',
            options={'ordering': ['owner_type', 'name']},
        ),
        migrations.AlterModelOptions(
            name='ownercontact',
            options={'ordering': ['name']},
        ),
    ]
