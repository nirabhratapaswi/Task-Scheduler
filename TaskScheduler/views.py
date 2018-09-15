from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
import datetime
import pytz
from .models import Task, Blocked, WeeklySchedule, DaysRepeated
from . import SlackRoundRobinScheduler as SRRS
from . import CRUD as crud
from . import schedulerAlgorithms as scAlgo
from . import forms as Forms
from django.utils.dateparse import parse_date
import json

calcutta = pytz.timezone("Asia/Calcutta")

def convertToDateTime(date_string, time_string, *args):
	date = datetime.datetime.strptime(date_string, "%m/%d/%Y").date()
	time = datetime.datetime.strptime(time_string+":00.00000", "%H:%M:%S.%f").time()
	return datetime.datetime.combine(date, time).replace(tzinfo=pytz.UTC)

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
	weekly_schedule = crud.getWeeklySchedulePerDayAsList()
	taskList = list()
	for t in tasks:
		taskList.append(t)

	blockedList = list()
	for b in blocked:
		blockedList.append(b)

	# schedule = scAlgo.scheduleTasks(taskList, blockedList)
	# current_time = SRRS.roundToNearestHour(timezone.now())
	tz = pytz.UTC
	current_time = SRRS.roundToNearestHour(tz.normalize(tz.localize(timezone.now().replace(tzinfo=None))).astimezone(pytz.timezone("Asia/Calcutta")).replace(tzinfo=pytz.UTC))
	print("Current Time: " + str(current_time))
	# current_time = pytz.timezone("Asia/Calcutta").localize(current_time.replace(tzinfo=None))
	schedule = SRRS.scheduleTasks(taskList, current_time, blockedList, weekly_schedule)

	print("Schedule: ")
	for s in schedule:
		print("Task name: " + s.task.name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time))

	# index = 0
	# for s in schedule:
	# 	s.start_time = s.start_time.isoformat()
	# 	s.end_time = s.end_time.isoformat()
	# 	schedule[index] = s
	# 	index += 1

	return render(request, 'schedule.html', {'schedule': schedule})

def createTask(request):
	if request.method == "POST":
		data = dict()
		print("Date: " + str(request.POST["deadline_date"]) + ", Time: " + str(request.POST["deadline_time"]))
		data["name"] = request.POST["name"]
		data["priority"] = request.POST["priority"]
		data["span"] = request.POST["span"]
		data["deadline"] = convertToDateTime(request.POST["deadline_date"], request.POST["deadline_time"])
		data["at_a_stretch"] = request.POST["at_a_stretch"]
		data["done"] = False
		data["max_repeats_per_day"] = request.POST["max_repeats_per_day"]
		data["times_repeated_today"] = 0
		data["break_needed_afterwards"] = request.POST["break_needed_afterwards"]
		# aware_datetime = datetime.datetime.strptime(data["deadline"]+":00", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
		# data["deadline"] = aware_datetime
		print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
		crud.createTask(name=data["name"], priority=data["priority"], span=data["span"], deadline=data["deadline"], at_a_stretch=data["at_a_stretch"], done=False, max_repeats_per_day=data["max_repeats_per_day"], times_repeated_today=data["times_repeated_today"], break_needed_afterwards=data["break_needed_afterwards"])
		return HttpResponse(json.dumps({"msg": "Task Created Successfully."}), content_type="application/json")
	else:
		return render(request, 'createTask.html', {'form': Forms.TaskForm})

def getTasks(request):
	# if this is a POST request we need to process the form data
	tasks = Task.objects.all()
	for t in tasks:
		print("Task Name: " + t.name)
	return render(request, 'taskList.html', {'tasks': tasks})

def deleteTask(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		data = request.POST
		print("Id: " + data["id"])
		# t = Task.objects.filter(pk=data["id"])
		# t.delete()
		crud.deleteTaskById(task_id=data["id"])
		return HttpResponse(json.dumps({"msg": "Task Deleted Successfully."}), content_type="application/json")
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		return HttpResponse("Non POST methods not supported.")

def createBlocked(request):
	if request.method=="POST":
		data = dict()
		data["name"] = request.POST["name"]
		# data["start_time"] = datetime.datetime.strptime(request.POST["start_time"], "%Y-%m-%dT%H:%M")
		# data["end_time"] = datetime.datetime.strptime(request.POST["end_time"], "%Y-%m-%dT%H:%M")
		# data["start_time"] = datetime.datetime.strptime(data["start_time"]+":00", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=calcutta)
		# data["end_time"] = datetime.datetime.strptime(data["end_time"]+":00", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=calcutta)
		data["start_time"] = convertToDateTime(request.POST["start_time_date"], request.POST["start_time_time"])
		data["end_time"] = convertToDateTime(request.POST["end_time_date"], request.POST["end_time_time"])
		# data["start_time"] = datetime.datetime.strptime(request.POST["start_time"]+":00", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
		# data["end_time"] = datetime.datetime.strptime(request.POST["end_time"]+":00", "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.UTC)
		print(data["name"]+", "+str(data["start_time"])+", "+str(data["end_time"]))
		# b = Blocked(name=data["name"], start_time=data["start_time"], end_time=data["end_time"])
		# b.save()
		crud.createBlocked(name=data["name"], start_time=data["start_time"], end_time=data["end_time"])
		return HttpResponse(json.dumps({"msg": "Blocked Task Created Successfully."}), content_type="application/json")
	else:
		return render(request, "createBlocked.html", {'form': Forms.BlockedForm})

def getBlocked(request):
	# if this is a POST request we need to process the form data
	blocked = Blocked.objects.all()
	for b in blocked:
		print("Blocked Name: " + b.name)
	return render(request, 'blockedList.html', {'blocked': blocked})

def deleteBlocked(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		data = request.POST
		print("Id: " + data["id"])
		# b = Blocked.objects.filter(pk=data["id"])
		# b.delete()
		crud.deleteBlockedById(blocked_id=data["id"])
		return HttpResponse(json.dumps({"msg": "Blocked Deleted Successfully."}), content_type="application/json")
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		return HttpResponse("Non POST methods not supported.")

def createWeeklySchedule(request):
	if request.method=="POST":
		data = dict()
		data["name"] = request.POST["name"]
		data["start_time"] = datetime.datetime.strptime(request.POST["start_time"]+":00.00000", "%H:%M:%S.%f").replace(tzinfo=pytz.UTC)
		data["end_time"] = datetime.datetime.strptime(request.POST["end_time"]+":00.00000", "%H:%M:%S.%f").replace(tzinfo=pytz.UTC)
		data["minimum_time_to_devote"] = request.POST["minimum_time_to_devote"]
		data["hard_bound"] = "hard_bound" in request.POST
		# days_repeated = [int(x) for x in request.POST.getlist("daysrepeated")]
		days_repeated = request.POST["days_repeated"].split(",")
		print("Days Repeated: ")
		print(days_repeated)
		print(data["name"]+", "+str(data["start_time"])+", "+str(data["end_time"]))
		# w = WeeklySchedule(name=data["name"], start_time=data["start_time"], end_time=data["end_time"])
		# w.save()
		crud.createWeeklySchedule(name=data["name"], start_time=data["start_time"], end_time=data["end_time"], days_repeated=days_repeated, minimum_time_to_devote=data["minimum_time_to_devote"], hard_bound=data["hard_bound"])
		return HttpResponse(json.dumps({"msg": "Weekly Schedule Created Successfully."}), content_type="application/json")
	else:
		return render(request, "createWeeklySchedule.html", {'form': Forms.WeeklyScheduleForm})

def getWeeklySchedule(request):
	# if this is a POST request we need to process the form data
	weekly_schedule = WeeklySchedule.objects.all()
	for w in weekly_schedule:
		print("Weekly Schedule Name: " + w.name)
	return render(request, 'weeklyScheduleList.html', {'weekly_schedule': weekly_schedule})

def deleteWeeklySchedule(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		data = request.POST
		print("Id: " + data["id"])
		# w = WeeklySchedule.objects.filter(pk=data["id"])
		# w.delete()
		crud.deleteWeeklyScheduleById(weekly_schedule_id=data["id"])
		return HttpResponse(json.dumps({"msg": "Weekly Schedule Deleted Successfully."}), content_type="application/json")
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		return HttpResponse("Non POST methods not supported.")
