# Generated by Django 3.0.5 on 2020-05-07 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20200505_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitlogger',
            name='date',
            field=models.DateField(),
        ),
    ]
