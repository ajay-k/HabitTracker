# Generated by Django 3.0.5 on 2020-05-05 03:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_habitlogger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitlogger',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]