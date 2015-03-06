# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0009_leaflet_reviewed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaflet',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
