# Generated by Django 2.2.20 on 2021-05-01 16:07

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("leaflets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaflet",
            name="ballots",
            field=django.db.models.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name="leaflet",
            name="people",
            field=django.db.models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name="leaflet",
            name="person_ids",
            field=django.db.models.JSONField(default=[]),
        ),
    ]
