from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Task, Blocked
from . import CRUD as crud
from . import schedulerAlgorithms as scAlgo
from .forms import TaskForm
from django.utils.dateparse import parse_date

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
		# print("Task name: " + s.task.name + ", duration: " + str((s.end_time - s.start_time).total_seconds()/60))

	return HttpResponse(response)

def createTask(request):
	if request.method == "POST":
		print("Post method called.")
		form = TaskForm(request.POST)
		form.is_valid()
		data = form.cleaned_data
		print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		print("Non post method called.")
	# return HttpResponse("Task created Successfully.")
	return render(request, 'task.html', {'form': TaskForm})

def get_task(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			return HttpResponseRedirect('/thanks/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()

	return render(request, 'name.html', {'form': form})
