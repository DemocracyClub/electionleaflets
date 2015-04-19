# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constituencies', '0002_auto_20150111_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constituency',
            name='count',
            field=models.IntegerField(null=True),
        ),
    ]
