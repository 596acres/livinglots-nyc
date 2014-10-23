# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0009_auto_20141001_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='borough',
            field=models.CharField(max_length=25, choices=[(b'Bronx', b'Bronx'), (b'Brooklyn', b'Brooklyn'), (b'Manhattan', b'Manhattan'), (b'Queens', b'Queens'), (b'Staten Island', b'Staten Island')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lot',
            name='owner_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='owners.OwnerContact', help_text='The contact for the owner of this lot.', null=True, verbose_name='owner contact'),
            preserve_default=True,
        ),
    ]
