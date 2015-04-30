# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groundtruth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groundtruthrecord',
            name='contact_email',
            field=models.EmailField(help_text='Who can we email for more information?', max_length=254, null=True, verbose_name='contact email', blank=True),
        ),
    ]
