from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
import datetime
import pytz
from .models import Task, Blocked, WeeklySchedule, DaysRepeated, Schedule
from . import SlackRoundRobinScheduler as SRRS
from . import CRUD as crud
from . import schedulerAlgorithms as scAlgo
from . import forms as Forms
from django.utils.dateparse import parse_date
import json
import os

class WeeklyScheduleTemp():
	def __init__(self, name, start_time, end_time):
		self.name = name
		self.start_time = start_time
		self.end_time = end_time

SERVER_URL = "http://localhost:8000"
if os.environ.get("SERVER_URL"):
	SERVER_URL = str(os.environ["SERVER_URL"])

print("SERVER_URL: " + SERVER_URL)

calcutta = pytz.timezone("Asia/Calcutta")

def convertToDateTime(date_string, time_string, *args):
	date = datetime.datetime.strptime(date_string, "%m/%d/%Y").date()
	time = datetime.datetime.strptime(time_string+":00.00000", "%H:%M:%S.%f").time()
	return datetime.datetime.combine(date, time).replace(tzinfo=pytz.UTC)

def getLocalTime(current_time_utc, *args):
	tz = pytz.UTC
	current_time_regional = SRRS.roundToNearestHour(tz.normalize(tz.localize((current_time_utc).replace(tzinfo=None))).astimezone(pytz.timezone("Asia/Calcutta")).replace(tzinfo=pytz.UTC))
	return current_time_regional

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

def reportUndoneTaskAsPerSchedule(request):
	current_time_utc = timezone.now()
	current_time_regional = getLocalTime(current_time_utc)	# + timezone.timedelta(minutes=360)
	if request.method == "POST":
		if request.POST["id"]:
			[success, error] = crud.updateScheduleStatus(request.POST["id"], current_time_regional, False)
			if success:
				return HttpResponse(json.dumps({"success": success, "msg": "Task maked as undone in timeline!"}), content_type="application/json")
			else:
				return HttpResponse(json.dumps({"success": success, "msg": error}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"success": False, "msg": "ID not mentioned in request!"}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({"success": False, "msg": "Get Method not Supported for this URL!"}), content_type="application/json")

def viewSchedule(request):
	schedule = crud.readSchedule()
	blocked = crud.readBlocked()
	weekly_schedule = crud.getWeeklySchedulePerDayAsList()
	# Logic to render weekly schedule
	current_time = min(schedule[0].start_time, blocked[0].start_time)
	weekly_schedule_list = list()
	index = 0
	schedule_length = len(schedule)
	for s in schedule:
		if index < schedule_length - 1:
			current_end_time = schedule[index].end_time	# or s.end_time
			next_start_time = schedule[index+1].start_time
			current_day = current_end_time.weekday()
			current_date = current_end_time.date()
			for w in weekly_schedule[current_day]:
				if w.weekly_schedule.hard_bound:
					if w.weekly_schedule.start_time >= current_end_time.time() and w.weekly_schedule.end_time <= next_start_time.time():
						weekly_schedule_list.append(WeeklyScheduleTemp(w.weekly_schedule.name, datetime.datetime.combine(current_date, w.weekly_schedule.start_time).replace(tzinfo=pytz.UTC), datetime.datetime.combine(current_date, w.weekly_schedule.end_time).replace(tzinfo=pytz.UTC)))
				else:
					if w.weekly_schedule.end_time <= next_start_time.time() and  (datetime.datetime.combine(current_date, w.weekly_schedule.end_time).replace(tzinfo=pytz.UTC) - current_end_time).total_seconds()/60 >= w.weekly_schedule.minimum_time_to_devote:
						weekly_schedule_list.append(WeeklyScheduleTemp(w.weekly_schedule.name, datetime.datetime.combine(current_date, w.weekly_schedule.start_time).replace(tzinfo=pytz.UTC), datetime.datetime.combine(current_date, w.weekly_schedule.end_time).replace(tzinfo=pytz.UTC)))
		index += 1
	print("Weekly Schedule list:")
	for w in weekly_schedule_list:
		print("Name: " + w.name + ", start_time: " + str(w.start_time) + ", end_time: " + str(w.end_time))
	return render(request, 'schedule.html', {
		'schedule': [s for s in schedule],
		'blocked': [b for b in blocked],
		'weekly_schedule': weekly_schedule_list,
		'SERVER_URL': SERVER_URL
	})

def prepareSchedule(request):	## Vimp - current timezone is set to India's, change it to take into account actual local timezone 
	for t in Task.objects.all():	# Added here so that reading schedule__task objects don't read old data
		t.times_repeated_today = 0
		t.left = t.span
		t.save()

	current_time_utc = timezone.now()
	current_time_regional = getLocalTime(current_time_utc)
	# current_time_regional -= timezone.timedelta(minutes=720)
	print("Current Regional Time: " + str(current_time_regional))
	schedules_till_now = crud.readPastSchedulesAsList(current_time_regional)
	# print("Past Schedules: " + str(len(schedules_till_now)))
	# for s in schedules_till_now:
	# 	print("Past Schedule name: " + s.task.name)
	max_end_time = current_time_regional
	for s in schedules_till_now:
		max_end_time = max(max_end_time, s.end_time)
		if s.task.done:
			s.task.left = 0
			s.task.save()
			continue
		if s.done:
			s.task.left -= (s.end_time - s.start_time).total_seconds()/60
			if s.task.left <= 0:
				s.task.done = True
			if s.end_time.weekday() == current_time_regional.weekday():
				s.task.times_repeated_today += 1
			s.task.save()

	current_time_regional = max(max_end_time, current_time_regional)
	tasks = crud.readUndoneTasks()
	blocked = crud.readBlocked(current_time_regional)
	weekly_schedule = crud.getWeeklySchedulePerDayAsList()
	taskList = list()
	for t in tasks:
		taskList.append(t)
	blockedList = list()
	for b in blocked:
		blockedList.append(b)

	schedule = SRRS.scheduleTasks(taskList, current_time_regional, blockedList, weekly_schedule)

	print("Schedule: ")
	for s in schedule:
		print("Task name: " + s.task.name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time))
		s.save()

	return HttpResponse(json.dumps({"success": True, "msg": "Schedule Created Successfully!"}), content_type="application/json")

def createTask(request):
	if request.method == "POST":
		data = dict()
		print("Date: " + str(request.POST["deadline_date"]) + ", Time: " + str(request.POST["deadline_time"]))
		if "id" in request.POST:
			data["id"] = request.POST["id"]
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
		if "id" in request.POST:
			[success, error] = crud.createTask(name=data["name"], priority=data["priority"], span=data["span"], deadline=data["deadline"], at_a_stretch=data["at_a_stretch"], done=False, max_repeats_per_day=data["max_repeats_per_day"], times_repeated_today=data["times_repeated_today"], break_needed_afterwards=data["break_needed_afterwards"], id=data["id"])
		else:
			[success, error] = crud.createTask(name=data["name"], priority=data["priority"], span=data["span"], deadline=data["deadline"], at_a_stretch=data["at_a_stretch"], done=False, max_repeats_per_day=data["max_repeats_per_day"], times_repeated_today=data["times_repeated_today"], break_needed_afterwards=data["break_needed_afterwards"])
		if success and "id" in request.POST:
			return HttpResponse(json.dumps({"msg": "Task Updated Successfully."}), content_type="application/json")
		elif success:
			return HttpResponse(json.dumps({"msg": "Task Created Successfully."}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"error": error}), content_type="application/json")
	else:
		return render(request, 'createTask.html', {
			'form': Forms.TaskForm,
			'SERVER_URL': SERVER_URL
		})

def getTasks(request):
	# if this is a POST request we need to process the form data
	tasks = crud.readAllTasks()
	return render(request, 'taskList.html', {
		'tasks': tasks,
		'SERVER_URL': SERVER_URL
	})

def deleteTask(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		data = request.POST
		print("Id: " + data["id"])
		# t = Task.objects.filter(pk=data["id"])
		# t.delete()
		[success, error] = crud.deleteTaskById(task_id=data["id"])
		if success:
			return HttpResponse(json.dumps({"msg": "Task Deleted Successfully."}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"error": error}), content_type="application/json")
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		return HttpResponse("Non POST methods not supported.")

def createBlocked(request):
	if request.method=="POST":
		data = dict()
		if "id" in request.POST:
			data["id"] = request.POST["id"]
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
		if "id" in request.POST:
			[success, error] = crud.createBlocked(name=data["name"], start_time=data["start_time"], end_time=data["end_time"], id=data["id"])
		else:
			[success, error] = crud.createBlocked(name=data["name"], start_time=data["start_time"], end_time=data["end_time"])
		if success:
			return HttpResponse(json.dumps({"msg": "Blocked Task Created Successfully."}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"error": error}), content_type="application/json")
	else:
		return render(request, "createBlocked.html", {
			'form': Forms.BlockedForm,
			'SERVER_URL': SERVER_URL
		})

def getBlocked(request):
	# if this is a POST request we need to process the form data
	blocked = crud.readBlocked()
	return render(request, 'blockedList.html', {
		'blocked': blocked,
		'SERVER_URL': SERVER_URL
	})

def deleteBlocked(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		data = request.POST
		print("Id: " + data["id"])
		# b = Blocked.objects.filter(pk=data["id"])
		# b.delete()
		[success, error] = crud.deleteBlockedById(blocked_id=data["id"])
		if success:
			return HttpResponse(json.dumps({"msg": "Blocked Deleted Successfully."}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"error": error}), content_type="application/json")
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		return HttpResponse("Non POST methods not supported.")

def createWeeklySchedule(request):
	if request.method=="POST":
		data = dict()
		if "id" in request.POST:
			data["id"] = request.POST["id"]
		data["name"] = request.POST["name"]
		data["start_time"] = datetime.datetime.strptime(request.POST["start_time"]+":00.00000", "%H:%M:%S.%f").replace(tzinfo=pytz.UTC).time()
		data["end_time"] = datetime.datetime.strptime(request.POST["end_time"]+":00.00000", "%H:%M:%S.%f").replace(tzinfo=pytz.UTC).time()
		data["minimum_time_to_devote"] = request.POST["minimum_time_to_devote"]
		data["hard_bound"] = False
		if "hard_bound" in request.POST:
			print("Value of hard_bound: " + str(request.POST["hard_bound"]) + ", type: " + str(type(request.POST["hard_bound"])))
			data["hard_bound"] = request.POST["hard_bound"] in ["True", "true", 1, "1", "Yes", "yes"]
		# days_repeated = [int(x) for x in request.POST.getlist("daysrepeated")]
		if "id" not in request.POST:
			days_repeated = request.POST["days_repeated"].split(",")
		print(data["name"]+", "+str(data["start_time"])+", "+str(data["end_time"]))
		# w = WeeklySchedule(name=data["name"], start_time=data["start_time"], end_time=data["end_time"])
		# w.save()
		if "id" in request.POST:
			[success, error] = crud.createWeeklySchedule(name=data["name"], start_time=data["start_time"], end_time=data["end_time"], days_repeated=list(), minimum_time_to_devote=data["minimum_time_to_devote"], hard_bound=data["hard_bound"], id=data["id"])
		else:
			[success, error] = crud.createWeeklySchedule(name=data["name"], start_time=data["start_time"], end_time=data["end_time"], days_repeated=days_repeated, minimum_time_to_devote=data["minimum_time_to_devote"], hard_bound=data["hard_bound"])
		if success:
			return HttpResponse(json.dumps({"msg": "Weekly Schedule Created Successfully."}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"error": error}), content_type="application/json")
	else:
		return render(request, "createWeeklySchedule.html", {
			'form': Forms.WeeklyScheduleForm,
			'SERVER_URL': SERVER_URL
		})

def getWeeklySchedule(request):
	# if this is a POST request we need to process the form data
	weekly_schedule = crud.readWeeklySchedule()
	return render(request, 'weeklyScheduleList.html', {
		'weekly_schedule': weekly_schedule,
		'SERVER_URL': SERVER_URL
	})

def deleteWeeklySchedule(request):
	# if this is a POST request we need to process the form data
	if request.method == "POST":
		data = request.POST
		print("Id: " + data["id"])
		# w = WeeklySchedule.objects.filter(pk=data["id"])
		# w.delete()
		[success, error] = crud.deleteWeeklyScheduleById(weekly_schedule_id=data["id"])
		if success:
			return HttpResponse(json.dumps({"msg": "Weekly Schedule Deleted Successfully."}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({"error": error}), content_type="application/json")
		# if form.is_valid():
		# 	data = form.cleaned_data
		# 	print(data["name"]+", "+str(data["priority"])+", "+str(data["span"])+", "+str(data["deadline"])+", "+str(data["at_a_stretch"]))
	else:
		return HttpResponse("Non POST methods not supported.")
