# Generated by Django 2.1.1 on 2018-09-04 18:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TaskScheduler', '0002_auto_20180903_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='at_a_stretch',
            field=models.IntegerField(default=60),
        ),
        migrations.AddField(
            model_name='task',
            name='left',
            field=models.IntegerField(default=60),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2018, 9, 5, 4, 20, 24, 879884, tzinfo=utc)),
        ),
    ]
