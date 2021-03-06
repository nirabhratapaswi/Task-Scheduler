from TaskScheduler.models import Task, Schedule, Blocked
from TaskScheduler.schedulerAlgorithms import *
from django.utils import *
import pytz
from django.utils.dateparse import parse_datetime

taskList = list()
for t in Task.objects.all():
	taskList.append(t)

blockedList = list()
for b in Blocked.objects.all():
	blockedList.append(b)

schedule = scheduleTasks(taskList, blockedList)

for s in schedule:
	print("Task name: " + s.task.name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time))
	# print("Task name: " + s.task.name + ", duration: " + str((s.end_time - s.start_time).total_seconds()/60))

Task(name="codechef", priority="2", span=60*4, deadline=timezone.now()+timezone.timedelta(days=10), at_a_stretch=60, left=60*4, done=False).save()
Task(name="codeforces", priority="2", span=60*3, deadline=timezone.now()+timezone.timedelta(days=10), at_a_stretch=60, left=60*3, done=False).save()
Task(name="badminton", priority="1", span=60*4, deadline=timezone.now()+timezone.timedelta(days=20), at_a_stretch=60, left=60*4, done=False).save()
Task(name="transport phenomena", priority="0", span=60*5, deadline=timezone.now()+timezone.timedelta(days=30), at_a_stretch=120, left=60*5, done=False).save()
Task(name="process engineering", priority="0", span=60*1, deadline=timezone.now()+timezone.timedelta(days=40), at_a_stretch=30, left=60*1, done=False).save()
Blocked(name="class", start_time=timezone.now()+timezone.timedelta(minutes=10), end_time=timezone.now()+timezone.timedelta(minutes=70)).save()
Blocked(name="sleep", start_time=timezone.now()+timezone.timedelta(minutes=100), end_time=timezone.now()+timezone.timedelta(minutes=150)).save()
Blocked(name="class", start_time=timezone.now()+timezone.timedelta(minutes=220), end_time=timezone.now()+timezone.timedelta(minutes=280)).save()
Blocked(name="class", start_time=pytz.timezone('UTC').localize(parse_datetime("2018-09-05 13:30:00"), is_dst=None), end_time=pytz.timezone('UTC').localize(parse_datetime("2018-09-05 14:00:00"), is_dst=None)).save()
Blocked(name="sleep", start_time=pytz.timezone('UTC').localize(parse_datetime("2018-09-05 16:00:00"), is_dst=None), end_time=pytz.timezone('UTC').localize(parse_datetime("2018-09-05 17:30:00"), is_dst=None)).save()
Blocked(name="class", start_time=pytz.timezone('UTC').localize(parse_datetime("2018-09-05 20:30:00"), is_dst=None), end_time=pytz.timezone('UTC').localize(parse_datetime("2018-09-05 22:00:00"), is_dst=None)).save()


# Test
from TaskScheduler.models import Task, Schedule, Blocked
# from TaskScheduler.schedulerAlgorithms import *
from TaskScheduler.SlackRoundRobinScheduler import *
from django.utils import *
import pytz
from django.utils.dateparse import parse_datetime

for t in Task.objects.all():
	t.delete()

for b in Blocked.objects.all():
	b.delete()

now = roundToNearestHour(timezone.now())
Task.objects.create(name="codechef", priority="2", span=60*4, deadline=now+timezone.timedelta(days=10), at_a_stretch=60, left=60*4, done=False)
Task.objects.create(name="badminton", priority="1", span=60*3, deadline=now+timezone.timedelta(days=20), at_a_stretch=60, left=60*3, done=False)
Task.objects.create(name="transport phenomena", priority="0", span=60*5, deadline=now+timezone.timedelta(days=30), at_a_stretch=120, left=60*5, done=False)
Blocked.objects.create(name="class", start_time=now+timezone.timedelta(minutes=60*2), end_time=now+timezone.timedelta(minutes=60*3))
Blocked.objects.create(name="sleep", start_time=now+timezone.timedelta(minutes=60*6+45), end_time=now+timezone.timedelta(minutes=60*7+45))

taskList = list()
for t in Task.objects.all():
	taskList.append(t)

blockedList = list()
for b in Blocked.objects.all():
	blockedList.append(b)

# schedule = scheduleTasks(taskList, blockedList)
current_time = timezone.now()
schedule = scheduleTasks(taskList, current_time, blockedList)

for s in schedule:
	print("Task name: " + s.task.name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time))
	# print("Task name: " + s.task.name + ", duration: " + str((s.end_time - s.start_time).total_seconds()/60))

# Test specifically for Handling Hard Deadlines
from TaskScheduler.models import Task, Schedule, Blocked
# from TaskScheduler.schedulerAlgorithms import *
from TaskScheduler.SlackRoundRobinScheduler import *
from django.utils import *
import pytz
from django.utils.dateparse import parse_datetime

for t in Task.objects.all():
	t.delete()

for b in Blocked.objects.all():
	b.delete()

now = roundToNearestHour(timezone.now())
Task.objects.create(name="codechef", priority="2", span=60*4, deadline=now+timezone.timedelta(minutes=60*7), at_a_stretch=60, left=60*4, done=False)
Task.objects.create(name="badminton", priority="1", span=60*5, deadline=now+timezone.timedelta(minutes=60*13), at_a_stretch=60, left=60*5, done=False)
Task.objects.create(name="transport phenomena", priority="0", span=60*5, deadline=now+timezone.timedelta(minutes=60*100), at_a_stretch=60, left=60*5, done=False)
Blocked.objects.create(name="class", start_time=now+timezone.timedelta(minutes=60*4), end_time=now+timezone.timedelta(minutes=60*5))
Blocked.objects.create(name="sleep", start_time=now+timezone.timedelta(minutes=60*12), end_time=now+timezone.timedelta(minutes=60*13+30))

taskList = list()
for t in Task.objects.all():
	taskList.append(t)

blockedList = list()
for b in Blocked.objects.all():
	blockedList.append(b)

# schedule = scheduleTasks(taskList, blockedList)
current_time = now
schedule = scheduleTasks(taskList, current_time, blockedList)

for s in schedule:
	print("Task name: " + s.task.name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time))
	# print("Task name: " + s.task.name + ", duration: " + str((s.end_time - s.start_time).total_seconds()/60))

