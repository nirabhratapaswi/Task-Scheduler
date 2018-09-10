from .models import Task, Schedule, Blocked, WeeklySchedule, DaysRepeated

def createTask(name, priority, span, deadline, at_a_stretch, done, *args):
	task = Task(name=name, priority=priority, span=span, deadline=deadline, at_a_stretch=at_a_stretch, left=span, done=done)
	task.save()
	return True	# TODO: write condition for saving and logical failured

def deleteTaskById(task_id, *args):
	task = Task.objects.get(pk=task_id)
	task.delete()
	return True

def deleteTaskByName(name, *args):
	task = Task.objects.get(name=name)
	task.delete()
	return True

def createBlocked(name, start_time, end_time, *args):	# check if slot is already booked!
	blocked = Blocked(name=name, start_time=start_time, end_time=end_time)
	blocked.save()
	return True	# TODO: write condition for saving and logical failured

def deleteBlockedById(blocked_id, *args):
	blocked = Blocked.objects.get(pk=blocked_id)
	blocked.delete()
	return True

def deleteBlockedByName(name, *args):
	blocked = Blocked.objects.get(name=name)
	blocked.delete()
	return True

def createWeeklySchedule(name, start_time, end_time, days_repeated, *args):	# check if slot is already booked!
	weekly_schedule = WeeklySchedule(name=name, start_time=start_time, end_time=end_time)
	weekly_schedule.save()
	for d in days_repeated:
		days_repeated = DaysRepeated(weekly_schedule=weekly_schedule, day_index=d)
		days_repeated.save()
	return True	# TODO: write condition for saving and logical failured

def deleteWeeklyScheduleById(weekly_schedule_id, *args):
	weekly_schedule = WeeklySchedule.objects.get(pk=weekly_schedule_id)
	weekly_schedule.delete()
	return True

def createDaysRepeated(weekly_schedule, day_index, *args):
	days_repeated = DaysRepeated(weekly_schedule=weekly_schedule, day_index=day_index)
	days_repeated.save()
	return True	# TODO: write condition for saving and logical failured

def deleteDaysRepeatedById(days_repeated_id, *args):
	days_repeated =	DaysRepeated.objects.get(pk=days_repeated_id)
	days_repeated.delete()
	return True

def saveSchedule(schedule_list, *args):
	for s in schedule_list:
		s.save()
	return True

def readUndoneTasks(*args):
	tasks = Task.objects.filter(done=False).order_by('-priority', 'name')
	return tasks

def readAllTasks(*args):
	tasks = Task.objects.all()
	return tasks

def readBlocked(*args):	# args[0] is time to start considering blocked tasks from, args[1] is time to end considering blocked tasks till
	if (len(args) == 2):
		blocked = Blocked.objects.filter(start_time__gt=args[0]).filter(end_time=args[1]).order_by('start_time')
	elif (len(args) == 1):
		blocked = Blocked.objects.filter(end_time__gt=args[0]).order_by('start_time')
	else:	
		blocked = Blocked.objects.all().order_by('start_time')
	return blocked

def readScheduleList(*args):
	schedule_list = list()
	for s in Schedule.objects.all().order_by('start_time'):
		schedule_list.append(s)

	return schedule_list

def getWeeklySchedulePerDayAsList(*args):
	weekly_schedule = list()
	for day in range(0, 7):
		weekly_schedule.append(DaysRepeated.objects.filter(day_index=day).order_by('weekly_schedule__start_time'))

	return weekly_schedule