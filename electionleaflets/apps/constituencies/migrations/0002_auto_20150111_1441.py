# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constituencies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constituency',
            name='count',
            field=models.IntegerField(),
        ),
    ]
