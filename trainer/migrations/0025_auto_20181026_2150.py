# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-26 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0024_remove_timeline_to_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='hours',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='timeline',
            name='trainee_cnt',
            field=models.CharField(max_length=10),
        ),
    ]