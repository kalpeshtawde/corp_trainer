# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-02 15:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0028_auto_20181102_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='to_date',
        ),
    ]
