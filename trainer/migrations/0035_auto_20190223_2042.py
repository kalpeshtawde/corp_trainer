# Generated by Django 2.1.3 on 2019-02-23 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0034_auto_20190223_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]