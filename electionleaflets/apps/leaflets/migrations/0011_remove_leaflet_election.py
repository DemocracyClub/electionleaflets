# Generated by Django 4.2.16 on 2024-12-09 13:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("leaflets", "0010_remove_leaflet_constituency"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leaflet",
            name="election",
        ),
    ]
