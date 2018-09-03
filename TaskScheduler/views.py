from django.http import HttpResponse
from django.shortcuts import render
from .models import Task, Blocked

# Create your views here.
def prioritySchedule(request):
	tasks = Task.objects.filter(done=False).order_by('-priority', 'task_name')
	for t in tasks:
		print("Task Name: " + t.task_name)

	return HttpResponse("Done Scheduling")
