# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-27 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0008_auto_20180716_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactform',
            name='verify',
            field=models.CharField(default='empty', max_length=50),
        ),
    ]
