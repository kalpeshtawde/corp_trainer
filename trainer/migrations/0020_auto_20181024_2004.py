# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-24 14:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0019_auto_20181023_2313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='profile',
        ),
    ]
