# Generated by Django 2.2.20 on 2021-05-01 16:55

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("leaflets", "0002_auto_20210501_1607"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leaflet",
            name="ballots",
            field=django.db.models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name="leaflet",
            name="people",
            field=django.db.models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="leaflet",
            name="person_ids",
            field=django.db.models.JSONField(default=list),
        ),
    ]
