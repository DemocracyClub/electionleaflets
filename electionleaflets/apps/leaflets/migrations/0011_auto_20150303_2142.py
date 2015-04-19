# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0010_auto_20150303_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leafletimage',
            name='image_type',
            field=models.CharField(blank=True, max_length=255, null=True, db_index=True, choices=[(b'1_front', b'Front'), (b'2_back', b'Back'), (b'3_inside', b'Inside'), (b'4_inprint', b'Inprint')]),
        ),
    ]
