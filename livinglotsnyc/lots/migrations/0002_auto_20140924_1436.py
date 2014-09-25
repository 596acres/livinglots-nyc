# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='accessible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='bbl',
            field=models.CharField(max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lot',
            name='block',
            field=models.IntegerField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lot',
            name='borough',
            field=models.CharField(max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lot',
            name='lot',
            field=models.IntegerField(),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lot',
            name='group',
            field=models.ForeignKey(related_name=b'lotgroup', on_delete=django.db.models.deletion.SET_NULL, verbose_name='group', blank=True, to='lots.LotGroup', null=True),
        ),
    ]
