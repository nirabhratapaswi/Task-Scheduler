from .models import Task, Blocked

def readUndoneTasks(*args):
	tasks = Task.objects.filter(done=False).order_by('-priority', 'task_name')
	return tasks

def allTasks(*args):
	tasks = Task.objects.all()
	return tasks
