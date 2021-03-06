# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-04 16:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0029_auto_20181102_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1000)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainer.Profile')),
            ],
        ),
    ]
