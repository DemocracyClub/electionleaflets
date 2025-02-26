# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 14:56


import django.utils.timezone
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LeafletProperties",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "key",
                    models.CharField(blank=True, db_index=True, max_length=100),
                ),
                (
                    "value",
                    models.CharField(blank=True, db_index=True, max_length=255),
                ),
            ],
            options={
                "abstract": False,
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
            },
        ),
    ]
