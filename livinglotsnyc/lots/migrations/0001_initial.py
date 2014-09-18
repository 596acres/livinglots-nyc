# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('livinglots_lots', '__first__'),
        ('owners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('centroid', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, verbose_name='centroid', blank=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, verbose_name='polygon', blank=True)),
                ('name', models.CharField(max_length=256, null=True, verbose_name='name', blank=True)),
                ('address_line1', models.CharField(max_length=150, null=True, verbose_name='address line 1', blank=True)),
                ('address_line2', models.CharField(max_length=150, null=True, verbose_name='address line 2', blank=True)),
                ('postal_code', models.CharField(max_length=10, null=True, verbose_name='postal code', blank=True)),
                ('city', models.CharField(max_length=50, null=True, verbose_name='city', blank=True)),
                ('state_province', models.CharField(max_length=40, null=True, verbose_name='state/province', blank=True)),
                ('country', models.CharField(max_length=40, null=True, verbose_name='country', blank=True)),
                ('known_use_certainty', models.PositiveIntegerField(default=0, help_text='On a scale of 0 to 10, how certain are we that the known use is correct?', verbose_name='known use certainty')),
                ('known_use_locked', models.BooleanField(default=False, help_text='Is the known use field locked? If it is not, the site will make a guess using available data. If you are certain that the known use is correct, lock it.', verbose_name='known use locked')),
                ('added', models.DateTimeField(help_text=b'When this lot was added', verbose_name='date added', auto_now_add=True)),
                ('added_reason', models.CharField(help_text=b'The original reason this lot was added', max_length=256, verbose_name='reason added')),
                ('steward_inclusion_opt_in', models.BooleanField(default=False, help_text='Did the steward opt in to being included on our map?', verbose_name='steward inclusion opt-in')),
                ('polygon_area', models.DecimalField(decimal_places=2, max_digits=15, blank=True, help_text='The area of the polygon in square feet', null=True, verbose_name='polygon area')),
                ('polygon_width', models.DecimalField(decimal_places=2, max_digits=10, blank=True, help_text='The width of the polygon in feet', null=True, verbose_name='polygon width')),
            ],
            options={
                'permissions': (('view_preview', 'Can view preview map'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LotGroup',
            fields=[
                ('lot_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='lots.Lot')),
            ],
            options={
                'abstract': False,
            },
            bases=('lots.lot', models.Model),
        ),
        migrations.AddField(
            model_name='lot',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='group', blank=True, to='lots.LotGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='known_use',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='livinglots_lots.Use', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lot',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='owners.Owner', help_text='The owner of this lot.', null=True, verbose_name='owner'),
            preserve_default=True,
        ),
    ]
