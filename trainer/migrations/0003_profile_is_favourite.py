# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-08 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0002_auto_20180908_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]
