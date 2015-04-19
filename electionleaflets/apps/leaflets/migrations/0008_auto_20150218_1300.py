# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0007_auto_20150218_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leafletimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(max_length=255, upload_to=b'leaflets'),
        ),
        migrations.AlterField(
            model_name='leafletimage',
            name='raw_image',
            field=sorl.thumbnail.fields.ImageField(max_length=255, upload_to=b'raw_leaflets', blank=True),
        ),
    ]
