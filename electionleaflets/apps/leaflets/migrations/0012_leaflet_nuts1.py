# Generated by Django 4.2.17 on 2024-12-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leaflets", "0011_remove_leaflet_election"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaflet",
            name="nuts1",
            field=models.CharField(blank=True, max_length=3),
        ),
    ]