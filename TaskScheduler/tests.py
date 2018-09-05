from django.test import TestCase, Client
from .models import Task, Schedule, Blocked
from .schedulerAlgorithms import roundToNearestHour, scheduleTasks
from django.utils import timezone
import pytz

# Create your tests here.
class ScheduleTests(TestCase):
	def setUp(self):
		self.now = roundToNearestHour(timezone.now())
		print("Time now: " + str(self.now))
		Task.objects.create(name="codechef", priority="2", span=60*4, deadline=self.now+timezone.timedelta(days=10), at_a_stretch=60, left=60*4, done=False)
		Task.objects.create(name="badminton", priority="1", span=60*3, deadline=self.now+timezone.timedelta(days=20), at_a_stretch=60, left=60*3, done=False)
		Task.objects.create(name="transport phenomena", priority="0", span=60*5, deadline=self.now+timezone.timedelta(days=30), at_a_stretch=120, left=60*5, done=False)
		Blocked.objects.create(name="class", start_time=self.now+timezone.timedelta(minutes=60*2), end_time=self.now+timezone.timedelta(minutes=60*3))
		Blocked.objects.create(name="sleep", start_time=self.now+timezone.timedelta(minutes=60*6+45), end_time=self.now+timezone.timedelta(minutes=60*7+45))

	def testScheduledCorrectly(self):
		print('Flag 3')
		taskList = list()
		for t in Task.objects.all():
			taskList.append(t)

		blockedList = list()
		for b in Blocked.objects.all():
			blockedList.append(b)

		schedule = scheduleTasks(taskList, blockedList)
		timedelta_dict = [{
			'name': "codechef",
			'start': self.now,
			'end': self.now + timezone.timedelta(minutes=60*1)
		}, {
			'name': "badminton",
			'start': self.now + timezone.timedelta(minutes=60*1),
			'end': self.now + timezone.timedelta(minutes=60*2)
		}, {
			'name': "transport phenomena",
			'start': self.now + timezone.timedelta(minutes=60*3),
			'end': self.now + timezone.timedelta(minutes=60*5)
		}, {
			'name': "codechef",
			'start': self.now + timezone.timedelta(minutes=60*5),
			'end': self.now + timezone.timedelta(minutes=60*6)
		}, {
			'name': "badminton",
			'start': self.now + timezone.timedelta(minutes=60*6),
			'end': self.now + timezone.timedelta(minutes=60*6+45)
		}, {
			'name': "transport phenomena",
			'start': self.now + timezone.timedelta(minutes=60*7+45),
			'end': self.now + timezone.timedelta(minutes=60*9+45)
		}, {
			'name': "codechef",
			'start': self.now + timezone.timedelta(minutes=60*9+45),
			'end': self.now + timezone.timedelta(minutes=60*10+45)
		}, {
			'name': "badminton",
			'start': self.now + timezone.timedelta(minutes=60*10+45),
			'end': self.now + timezone.timedelta(minutes=60*11+45)
		}, {
			'name': "transport phenomena",
			'start': self.now + timezone.timedelta(minutes=60*11+45),
			'end': self.now + timezone.timedelta(minutes=60*12+45)
		}, {
			'name': "codechef",
			'start': self.now + timezone.timedelta(minutes=60*12+45),
			'end': self.now + timezone.timedelta(minutes=60*13+45)
		}, {
			'name': "badminton",
			'start': self.now + timezone.timedelta(minutes=60*13+45),
			'end': self.now + timezone.timedelta(minutes=60*14)
		}]
		# schedule_test = [Schedule(task=Task.objects.get(name=codechef), start_time=self.now()+timezone.timedelta(), end_time=)]

		i = 0
		for s in schedule:
			print("Task name: " + s.task.name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time))
			self.assertEqual(s.task.name, timedelta_dict[i]["name"])
			self.assertEqual(s.start_time, timedelta_dict[i]["start"])
			self.assertEqual(s.end_time, timedelta_dict[i]["end"])
			# print("Timedelta: start time: " + str(timedelta_dict[i]["start"]) + ", end: " + str(timedelta_dict[i]["end"]))
			# print("Task name: " + s.task.name + ", duration: " + str((s.end_time - s.start_time).total_seconds()/60))
			i += 1

		self.assertEqual(True, True)

	def tearDown(self):
		print("Finishing testing the Scheduling...")
