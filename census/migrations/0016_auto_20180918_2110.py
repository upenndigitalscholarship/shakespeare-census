# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-09-18 21:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0015_auto_20180918_2109'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdetail',
            old_name='affiliation',
            new_name='affiliation_str',
        ),
    ]
