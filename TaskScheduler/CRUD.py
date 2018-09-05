from .models import Task, Schedule, Blocked

def createTask(name, priority, span, deadline, at_a_stretch, done, *args):
	task = Task(name=name, priority=priority, span=span, at_a_stretch=at_a_stretch, left=span, done=done)
	task.save()
	return True	# TODO: write condition for saving and logical failured

def deleteTaskById(taskId, *args):
	task = Task.objects.get(pk=taskId)
	task.delete()
	return True

def deleteTaskByName(name, *args):
	task = Task.objects.get(name=name)
	task.delete()
	return True

def createBlocked(name, start_time, end_time, *args):
	blocked = Blocked(name=name, start_time=start_time, end_time=end_time)
	blocked.save()
	return True	# TODO: write condition for saving and logical failured

def deleteBlockedById(blockedId, *args):
	blocked = Blocked.objects.get(pk=blockedId)
	blocked.delete()
	return True

def deleteBlockedByName(name, *args):
	blocked = Blocked.objects.get(name=name)
	blocked.delete()
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
		blocked = Blocked.objects.filter(start_time__gt=args[0]).order_by('start_time')
	else:	
		blocked = Blocked.objects.all().order_by('start_time')
	return blocked

def readScheduleList(*args):
	schedule_list = list()
	for s in Schedule.objects.all().order_by('start_time'):
		schedule_list.append(s)

	return schedule_list
