# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20150324_0859'),
        ('leaflets', '0013_leaflet_election'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaflet',
            name='publisher_person',
            field=models.ForeignKey(blank=True, to='people.Person', null=True),
            preserve_default=True,
        ),
    ]
