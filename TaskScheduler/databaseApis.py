from .models import Task, Blocked

def readUndoneTasks(*args):
	tasks = Task.objects.filter(done=False).order_by('-priority', 'name')
	return tasks

def allTasks(*args):
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

