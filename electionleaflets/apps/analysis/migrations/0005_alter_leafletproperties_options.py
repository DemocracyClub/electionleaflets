# Generated by Django 4.0.3 on 2024-09-16 13:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("analysis", "0004_auto_20210424_1221"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="leafletproperties",
            options={"get_latest_by": "modified"},
        ),
    ]
