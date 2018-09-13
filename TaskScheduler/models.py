from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Task(models.Model):
	def __str__(self):
		return self.name + " (" + str(self.priority) + ")"

	choices = (("0", "Low"), ("1", "Medium"), ("2", "High"))

	name = models.CharField(max_length=200)
	priority = models.CharField(max_length=10, default="0", choices=choices)	# 0->low 1-> medium 2-> high
	span = models.IntegerField(default=60)
	deadline = models.DateTimeField(default=(timezone.now()+timezone.timedelta(minutes=10*60)))
	at_a_stretch = models.IntegerField(default=60)	# how much time you need to do this task once started (in one sitting)
	left = models.IntegerField(default=60)	# time left to complete the task
	done = models.BooleanField(default=False)
	max_repreats_per_day = models.IntegerField(default=4)
	break_needed_afterwards = models.IntegerField(default=15)

class Schedule(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	start_time = models.DateTimeField(default=timezone.now()+timezone.timedelta(minutes=60))
	end_time = models.DateTimeField(default=(timezone.now()+timezone.timedelta(minutes=10*60)))

class Blocked(models.Model):	# Specially booked time slots
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200, default=None)
	start_time = models.DateTimeField(default=timezone.now()+timezone.timedelta(minutes=60))
	end_time = models.DateTimeField(default=(timezone.now()+timezone.timedelta(minutes=10*60)))

class WeeklySchedule(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)
	start_time = models.TimeField(default=(timezone.now()+timezone.timedelta(minutes=60)).time())
	end_time = models.TimeField(default=(timezone.now()+timezone.timedelta(minutes=10*60)).time())
	minimum_time_to_devote = models.IntegerField(default=30)
	hard_bound = models.BooleanField(default=True)

class DaysRepeated(models.Model):
	weekly_schedule = models.ForeignKey(WeeklySchedule, on_delete=models.CASCADE)
	day_index = models.IntegerField(default=0)
