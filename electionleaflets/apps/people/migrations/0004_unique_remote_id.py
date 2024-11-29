# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-02 22:44


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("people", "0003_remove_duplicates"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="remote_id",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True
            ),
        ),
    ]
