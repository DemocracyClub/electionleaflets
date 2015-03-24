# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '__first__'),
        ('constituencies', '0003_auto_20150111_1441'),
        ('uk_political_parties', '0004_auto_20150322_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartyMemberships',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('membership_start', models.DateField()),
                ('membership_end', models.DateField()),
                ('party', models.ForeignKey(to='uk_political_parties.Party')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('remote_id', models.CharField(max_length=255, null=True, blank=True)),
                ('source_url', models.URLField(null=True, blank=True)),
                ('image_url', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonConstituencies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('constituency', models.ForeignKey(to='constituencies.Constituency')),
                ('election', models.ForeignKey(to='elections.Election')),
                ('person', models.ForeignKey(to='people.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='constituencies',
            field=models.ManyToManyField(to='constituencies.Constituency', through='people.PersonConstituencies'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='elections',
            field=models.ManyToManyField(to='elections.Election'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='parties',
            field=models.ManyToManyField(to='uk_political_parties.Party', through='people.PartyMemberships'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partymemberships',
            name='person',
            field=models.ForeignKey(to='people.Person'),
            preserve_default=True,
        ),
    ]
