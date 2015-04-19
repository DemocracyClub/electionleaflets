# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0008_auto_20150218_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaflet',
            name='reviewed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
