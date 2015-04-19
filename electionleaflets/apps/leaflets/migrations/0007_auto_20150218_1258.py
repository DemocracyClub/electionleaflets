# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0006_auto_20150217_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaflet',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
