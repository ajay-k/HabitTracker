# Generated by Django 3.0.5 on 2020-05-07 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20200507_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habitlogger',
            name='completed',
        ),
    ]