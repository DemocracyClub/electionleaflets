# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0002_leafletimage_image_text'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UploadSession',
        ),
        migrations.AlterModelOptions(
            name='leaflet',
            options={'ordering': ('date_uploaded',)},
        ),
        migrations.AddField(
            model_name='leafletimage',
            name='raw_image',
            field=sorl.thumbnail.fields.ImageField(default='', upload_to=b'raw_leaflets'),
            preserve_default=False,
        ),
    ]
