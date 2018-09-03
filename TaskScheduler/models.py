from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Task(models.Model):
	def __str__(self):
		return self.task_name + " (" + str(self.priority) + ")"

	choices = (("0", "Low"), ("1", "Medium"), ("2", "High"))

	task_name = models.CharField(max_length=200)
	priority = models.CharField(max_length=10, default="0", choices=choices)	# 0->low 1-> medium 2-> high
	span = models.IntegerField(default=60)
	deadline = models.DateField(default=(timezone.now()+timezone.timedelta(minutes=10*60)))
	done = models.BooleanField(default=False)

class Schedule(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	start_time = models.DateField()
	end_time = models.DateField()

class Blocked(models.Model):
	start_time = models.DateField()
	end_time = models.DateField()
