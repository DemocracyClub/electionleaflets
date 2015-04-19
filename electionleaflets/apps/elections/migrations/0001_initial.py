# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('live_date', models.DateTimeField()),
                ('dead_date', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('country', models.ForeignKey(blank=True, to='core.Country', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
