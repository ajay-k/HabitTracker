# Generated by Django 3.0.5 on 2020-05-11 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_habitlogger_current_total_habits'),
    ]

    operations = [
        migrations.RenameField(
            model_name='habit',
            old_name='description',
            new_name='goal',
        ),
        migrations.AddField(
            model_name='habit',
            name='completed_count',
            field=models.IntegerField(default=0),
        ),
    ]
