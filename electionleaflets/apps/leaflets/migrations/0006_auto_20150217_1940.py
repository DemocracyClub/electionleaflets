# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0004_auto_20150213_1715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaflet',
            options={'ordering': ('-date_uploaded',)},
        ),
        migrations.AlterField(
            model_name='leaflet',
            name='date_uploaded',
            field=models.DateTimeField(),
        ),
    ]
