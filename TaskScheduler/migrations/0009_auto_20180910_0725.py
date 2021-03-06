# Generated by Django 2.1.1 on 2018-09-10 07:25

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('TaskScheduler', '0008_auto_20180909_0720'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysRepeated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_index', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklySchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_time', models.TimeField(default=datetime.time(8, 25, 40, 594456))),
                ('end_time', models.TimeField(default=datetime.time(17, 25, 40, 594479))),
            ],
        ),
        migrations.AlterField(
            model_name='blocked',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 10, 17, 25, 40, 594165, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='blocked',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 10, 8, 25, 40, 594142, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 10, 17, 25, 40, 593767, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 10, 8, 25, 40, 593738, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 10, 17, 25, 40, 584026, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='daysrepeated',
            name='weekly_schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TaskScheduler.WeeklySchedule'),
        ),
    ]
