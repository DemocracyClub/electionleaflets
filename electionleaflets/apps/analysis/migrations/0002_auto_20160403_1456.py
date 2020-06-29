# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 14:56


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("analysis", "0001_initial"),
        ("leaflets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="leafletproperties",
            name="leaflet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="leaflets.Leaflet",
            ),
        ),
        migrations.AddField(
            model_name="leafletproperties",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
