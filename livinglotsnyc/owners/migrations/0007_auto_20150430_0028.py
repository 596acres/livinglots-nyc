# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owners', '0006_auto_20150430_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='aliases',
            field=models.ManyToManyField(help_text='Other names for this owner', to='livinglots_owners.Alias', verbose_name='aliases', blank=True),
        ),
    ]
