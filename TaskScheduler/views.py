from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Task, Blocked
from . import databaseApis as dbApis
from . import schedulerAlgorithms as scAlgo

# Create your views here.
def prioritySchedule(request):
	tasks = dbApis.readUndoneTasks()
	blocked = dbApis.readBlocked(timezone.now())
	taskList = list()
	for t in tasks:
		taskList.append(t)

	blockedList = list()
	for b in blocked:
		blockedList.append(b)

	schedule = scAlgo.scheduleTasks(taskList, blockedList)
	response = ""
	i = 0
	for s in schedule:
		i += 1
		response += str(i) + ") Task name: " + s.task.name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time) + "<br>"
		# print("Task name: " + s.task.name + ", duration: " + str((s.end_time - s.start_time).total_seconds()/60))

	return HttpResponse(response)
