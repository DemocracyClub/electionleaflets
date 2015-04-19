# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leafletimage',
            name='image_text',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
