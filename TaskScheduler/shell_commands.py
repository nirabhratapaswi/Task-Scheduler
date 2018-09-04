from TaskScheduler.models import Task, Schedule, Blocked
from TaskScheduler.schedulerAlgorithms import *
from django.utils import *

taskList = list()
for t in Task.objects.all():
	taskList.append(t)

blockedList = list()
for b in Blocked.objects.all():
	blockedList.append(b)

schedule = scheduleTasks(taskList, blockedList)

for s in schedule:
	print("Task name: " + s.task.task_name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time))

Task(task_name="codechef", priority="2", span=60*4, deadline=timezone.now()+timezone.timedelta(days=10), at_a_stretch=60, left=60*4, done=False).save()
Task(task_name="codeforces", priority="2", span=60*3, deadline=timezone.now()+timezone.timedelta(days=10), at_a_stretch=60, left=60*3, done=False).save()
Task(task_name="badminton", priority="1", span=60*4, deadline=timezone.now()+timezone.timedelta(days=20), at_a_stretch=60, left=60*4, done=False).save()
Task(task_name="transport phenomena", priority="0", span=60*5, deadline=timezone.now()+timezone.timedelta(days=30), at_a_stretch=120, left=60*5, done=False).save()
Task(task_name="process engineering", priority="0", span=60*1, deadline=timezone.now()+timezone.timedelta(days=40), at_a_stretch=30, left=60*1, done=False).save()
