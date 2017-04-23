# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 14:56
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('elections', '0001_initial'),
        ('constituencies', '0001_initial'),
        ('uk_political_parties', '0004_auto_20150322_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaflet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=765)),
                ('description', models.TextField(blank=True, null=True)),
                ('imprint', models.TextField(blank=True, null=True)),
                ('postcode', models.CharField(blank=True, max_length=150)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('name', models.CharField(blank=True, max_length=300)),
                ('email', models.CharField(blank=True, max_length=300)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('date_delivered', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('live', 'Live'), ('draft', 'Draft'), ('removed', 'Removed')], max_length=255, null=True)),
                ('reviewed', models.BooleanField(default=False)),
                ('constituency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='constituencies.Constituency')),
                ('election', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elections.Election')),
                ('publisher_party', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='uk_political_parties.Party')),
            ],
            options={
                'ordering': ('-date_uploaded',),
            },
        ),
        migrations.CreateModel(
            name='LeafletImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(max_length=255, upload_to='leaflets')),
                ('raw_image', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='raw_leaflets')),
                ('legacy_image_key', models.CharField(blank=True, max_length=255)),
                ('image_type', models.CharField(blank=True, choices=[('1_front', 'Front'), ('2_back', 'Back'), ('3_inside', 'Inside'), ('4_inprint', 'Inprint')], max_length=255, null=True)),
                ('image_text', models.TextField(blank=True)),
                ('leaflet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='leaflets.Leaflet')),
            ],
            options={
                'ordering': ['image_type'],
            },
        ),
    ]
