# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0003_auto_20150213_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leafletcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='leafletcategory',
            name='leaflet',
        ),
        migrations.RemoveField(
            model_name='leaflettag',
            name='leaflet',
        ),
        migrations.RemoveField(
            model_name='leaflettag',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Promise',
        ),
        migrations.DeleteModel(
            name='RateInteresting',
        ),
        migrations.DeleteModel(
            name='RateInterestingSeq',
        ),
        migrations.DeleteModel(
            name='RateType',
        ),
        migrations.DeleteModel(
            name='RateValue',
        ),
        migrations.DeleteModel(
            name='RateValueSeq',
        ),
        migrations.RemoveField(
            model_name='leaflet',
            name='attacks',
        ),
        migrations.RemoveField(
            model_name='leaflet',
            name='categories',
        ),
        migrations.DeleteModel(
            name='LeafletCategory',
        ),
        migrations.RemoveField(
            model_name='leaflet',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='leaflet',
            name='lng',
        ),
        migrations.RemoveField(
            model_name='leaflet',
            name='tags',
        ),
        migrations.DeleteModel(
            name='LeafletTag',
        ),
        migrations.AddField(
            model_name='leaflet',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leafletimage',
            name='legacy_image_key',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='leafletimage',
            name='raw_image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'raw_leaflets', blank=True),
        ),
    ]
