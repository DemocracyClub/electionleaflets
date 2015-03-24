# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_person_source_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partymemberships',
            name='membership_end',
            field=models.DateField(null=True),
        ),
    ]
