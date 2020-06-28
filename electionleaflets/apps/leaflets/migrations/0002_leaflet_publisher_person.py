# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 14:56


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
        ('leaflets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaflet',
            name='publisher_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='people.Person'),
        ),
    ]
