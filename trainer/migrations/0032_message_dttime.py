# Generated by Django 2.1.3 on 2019-01-10 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0031_message_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='dttime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]