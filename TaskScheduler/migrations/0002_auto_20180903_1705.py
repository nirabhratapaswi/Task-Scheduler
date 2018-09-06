# Generated by Django 2.1.1 on 2018-09-03 17:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TaskScheduler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2018, 9, 4, 3, 5, 41, 60542, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='span',
            field=models.IntegerField(default=60),
        ),
    ]