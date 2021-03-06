# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-18 21:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0014_auto_20180918_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='affiliation_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='census.Location'),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='affiliation',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
