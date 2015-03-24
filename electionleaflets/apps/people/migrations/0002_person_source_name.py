# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='source_name',
            field=models.CharField(default='YNMP', max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
