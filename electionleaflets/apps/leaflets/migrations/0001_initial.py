# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import leaflets.models


class Migration(migrations.Migration):

    dependencies = [
        ('constituencies', '0003_auto_20150111_1441'),
        ('categories', '__first__'),
        ('tags', '__first__'),
        ('uk_political_parties', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaflet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=765, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('imprint', models.TextField(null=True, blank=True)),
                ('postcode', models.CharField(max_length=150, blank=True)),
                ('lng', models.FloatField(null=True, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('name', models.CharField(max_length=300, blank=True)),
                ('email', models.CharField(max_length=300, blank=True)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('date_delivered', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True, choices=[(b'live', b'Live'), (b'draft', b'Draft'), (b'removed', b'Removed')])),
                ('attacks', models.ManyToManyField(related_name=b'attacks', null=True, to='uk_political_parties.Party', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeafletCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='categories.Category')),
                ('leaflet', models.ForeignKey(to='leaflets.Leaflet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeafletImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'leaflets')),
                ('legacy_image_key', models.CharField(max_length=255)),
                ('image_type', models.CharField(blank=True, max_length=255, null=True, choices=[(b'1_front', b'Front'), (b'2_back', b'Back'), (b'3_inside', b'Inside'), (b'4_inprint', b'Inprint')])),
                ('leaflet', models.ForeignKey(related_name=b'images', to='leaflets.Leaflet')),
            ],
            options={
                'ordering': ['image_type'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeafletTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('leaflet', models.ForeignKey(to='leaflets.Leaflet')),
                ('tag', models.ForeignKey(to='tags.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Promise',
            fields=[
                ('promise_id', models.IntegerField(serialize=False, primary_key=True)),
                ('leaflet_id', models.IntegerField()),
                ('detail', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RateInteresting',
            fields=[
                ('rate_interesting_id', models.IntegerField(serialize=False, primary_key=True)),
                ('leaflet_id', models.IntegerField()),
                ('description', models.TextField()),
                ('user_name', models.CharField(max_length=765)),
                ('user_email', models.CharField(max_length=765)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RateInterestingSeq',
            fields=[
                ('sequence', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RateType',
            fields=[
                ('rate_type_id', models.IntegerField(serialize=False, primary_key=True)),
                ('left_label', models.CharField(max_length=150)),
                ('right_label', models.CharField(max_length=150, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RateValue',
            fields=[
                ('rate_value_id', models.IntegerField(serialize=False, primary_key=True)),
                ('leaflet_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=300)),
                ('user_email', models.CharField(max_length=300)),
                ('rate_type_id', models.IntegerField()),
                ('value', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RateValueSeq',
            fields=[
                ('sequence', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=64, null=True, blank=True)),
                ('image1', models.ImageField(max_length=255, null=True, upload_to='leaflets.models.update_filename', blank=True)),
                ('image2', models.ImageField(max_length=255, null=True, upload_to='leaflets.models.update_filename', blank=True)),
                ('image3', models.ImageField(max_length=255, null=True, upload_to='leaflets.models.update_filename', blank=True)),
                ('image4', models.ImageField(max_length=255, null=True, upload_to='leaflets.models.update_filename', blank=True)),
                ('image5', models.ImageField(max_length=255, null=True, upload_to='leaflets.models.update_filename', blank=True)),
                ('image6', models.ImageField(max_length=255, null=True, upload_to='leaflets.models.update_filename', blank=True)),
                ('image7', models.ImageField(max_length=255, null=True, upload_to='leaflets.models.update_filename', blank=True)),
                ('image8', models.ImageField(max_length=255, null=True, upload_to='leaflets.models.update_filename', blank=True)),
                ('s3keys', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='leaflet',
            name='categories',
            field=models.ManyToManyField(to='categories.Category', through='leaflets.LeafletCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaflet',
            name='constituency',
            field=models.ForeignKey(blank=True, to='constituencies.Constituency', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaflet',
            name='publisher_party',
            field=models.ForeignKey(blank=True, to='uk_political_parties.Party', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='leaflet',
            name='tags',
            field=models.ManyToManyField(to='tags.Tag', through='leaflets.LeafletTag'),
            preserve_default=True,
        ),
    ]
