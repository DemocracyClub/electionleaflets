# Generated by Django 4.2.16 on 2024-12-09 13:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("elections", "0001_initial"),
        ("leaflets", "0011_remove_leaflet_election"),
        ("people", "0007_remove_personconstituencies_constituency_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Election",
        ),
    ]