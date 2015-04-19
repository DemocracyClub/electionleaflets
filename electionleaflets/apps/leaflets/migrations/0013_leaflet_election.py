# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0001_initial'),
        ('leaflets', '0012_auto_20150322_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaflet',
            name='election',
            field=models.ForeignKey(to='elections.Election', null=True),
            preserve_default=True,
        ),
    ]
