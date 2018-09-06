from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from .models import Task, Blocked
from . import CRUD as crud
from . import schedulerAlgorithms as scAlgo
from .forms import TaskForm
from django.utils.dateparse import parse_date
import json

# Create your views here.
def prioritySchedule(request):
	tasks = crud.readUndoneTasks()
	blocked = crud.readBlocked(timezone.now())
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
		s.save()
		# print("Task name: " + s.task.name + ", duration: " + str((s.end_time - s.start_time).total_seconds()/60))

	return HttpResponse(response)
	# return render(request, 'schedule.html', {'schedule': schedule})

def schedule(request):
	tasks = crud.readUndoneTasks()
	blocked = crud.readBlocked(timezone.now())
	taskList = list()
	for t in tasks:
		taskList.append(t)

	blockedList = list()
	for b in blocked:
		blockedList.append(b)

	schedule = scAlgo.scheduleTasks(taskList, blockedList)

	return render(request, 'schedule.html', {'schedule': schedule})

def createTask(request):
	if request.method == "POST":
		print("Post method called.")
		form = TaskForm(request.POST)
		form.is_valid()
		data = form.cleaned_data
		print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
		t = Task(name=data["name"], priority=data["priority"], span=data["span"], deadline=data["deadline"], at_a_stretch=data["at_a_stretch"], left=data["span"], done=False)
		# t.save()
		return HttpResponse("Task created Successfully.")
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		print("Non post method called.")
		return render(request, 'createTask.html', {'form': TaskForm})

def getTasks(request):
	# if this is a POST request we need to process the form data
	tasks = Task.objects.all()
	for t in tasks:
		print("Task Name: " + t.name)
	return render(request, 'taskList.html', {'tasks': tasks})

def deleteTask(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		print("Post method called.")
		form = TaskForm(request.POST)
		form.is_valid()
		data = request.POST
		print("Id: " + data["id"])
		t = Task.objects.filter(pk=data["id"])
		t.delete()
		return HttpResponse(json.dumps({"msg": "Task deleted Successfully."}), content_type="application/json")
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		print("Non post method called.")
		return HttpResponse("Non POST methods not supported.")

