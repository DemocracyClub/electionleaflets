# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-15 16:14


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaflets', '0006_add_ynr_idxes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaflet',
            name='ballot_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]
