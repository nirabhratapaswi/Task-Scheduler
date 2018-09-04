from django.http import HttpResponse
from django.shortcuts import render
from .models import Task, Blocked
from . import databaseApis as dbApis
from . import schedulerAlgorithms as scAlgo

# Create your views here.
def prioritySchedule(request):
	tasks = dbApis.readUndoneTasks()
	for t in tasks:
		print("Task Name: " + t.task_name + ", priority: " + t.priority)

	return HttpResponse("Done Scheduling")
