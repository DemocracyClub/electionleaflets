# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('constituency_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=765)),
                ('country_name', models.CharField(max_length=255)),
                ('alternative_name', models.CharField(max_length=765, blank=True)),
                ('retired', models.IntegerField(null=True, blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, separator='_', blank=True)),
                ('count', models.IntegerField(null=True)),
                ('wikipedia_url', models.CharField(max_length=765, blank=True)),
                ('url_id', models.CharField(max_length=300, blank=True)),
                ('guardian_aristotle_id', models.IntegerField(null=True, blank=True)),
                ('guardian_pa_code', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Constituencies',
            },
            bases=(models.Model,),
        ),
    ]
