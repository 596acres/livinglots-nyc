# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0004_lot_owner_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('lots', models.ManyToManyField(to='lots.Lot')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
