from .models import Task, Schedule, Blocked
from django.utils import timezone
import pytz

def roundToNearestHour(time, *args):
	if time.minute > 0 and time.minute <= 30:
		time -= timezone.timedelta(minutes=time.minute, seconds=time.second)
		time = time.replace(minute=30, microsecond=0)
	else:
		time -= timezone.timedelta(hours=-1, minutes=time.minute, seconds=time.second)
		time = time.replace(minute=0, microsecond=0)
	return time

def isFreeFor(current_time, task, blocked_list, *args):	# blocked_list is sorted in ascending order
	is_free_for = 0
	blocked_till = current_time
	if len(blocked_list) == 0:
		# print("Flag 5.0")
		is_free_for = task.span
		blocked_till = current_time+timezone.timedelta(minutes=task.span)
		return [is_free_for, blocked_till]
	if current_time < blocked_list[0].start_time:
		# print("Flag 5.1")
		is_free_for = (blocked_list[0].start_time - current_time).total_seconds()/60
		blocked_till = None
		return [is_free_for, blocked_till]

	for i in range(0, len(blocked_list)-1):
		if current_time >= blocked_list[i].end_time and current_time < blocked_list[i+1].start_time:
			# print("Flag 5.2")
			is_free_for = (blocked_list[i+1].start_time - current_time).total_seconds()/60
			blocked_till = None
			break
		if current_time >= blocked_list[i].start_time and current_time < blocked_list[i].end_time:
			# print("Flag 5.3")
			is_free_for = 0
			blocked_till = blocked_list[i].end_time
			break

	if current_time >= blocked_list[len(blocked_list)-1].end_time:
		# print("Flag 5.4")
		is_free_for = task.span
		blocked_till = current_time+timezone.timedelta(minutes=task.span)
		return [is_free_for, blocked_till]
	elif current_time >= blocked_list[len(blocked_list)-1].start_time and current_time < blocked_list[len(blocked_list)-1].end_time:
		# print("Flag 5.5")
		is_free_for = 0
		blocked_till = blocked_list[len(blocked_list)-1].end_time

	return [is_free_for, blocked_till]

def scheduleTasks(task_list, blocked_list, *args):	# task_list is assumed to be Sorted sequentially by some logic, blocked_list is sorted in ascending order
	schedule = list()
	current_time = timezone.now()
	for s in Schedule.objects.all():
		s.delete()
	# pytz_obj.replace(tzinfo=pytz.timezone(pytz_zone))
	# current_time = pytz.timezone(pytz_zone).localize(timezone.now(), is_dst=None)
	current_time = roundToNearestHour(current_time)
	done = [False for x in range(0, len(task_list))]
	done_task_list = [None]*len(task_list)
	while False in done:
		# print(done)
		task_index = 0
		for task in task_list:
			if not done[task_index]:
				# print("For task: " + task.name)
				[is_free_for, blocked_till] = isFreeFor(current_time, task, blocked_list)
				# print("is_free_for: " + str(is_free_for) + ", blocked_till: " + str(blocked_till))
				while is_free_for == 0:
					current_time = blocked_till
					[is_free_for, blocked_till] = isFreeFor(current_time, task, blocked_list)
					# print("is_free_for: " + str(is_free_for) + ", blocked_till: " + str(blocked_till))

				if is_free_for >= task.left:
					if task.left > task.at_a_stretch:
						# print("Hack 1")
						task.left -= task.at_a_stretch
						schedule.append(Schedule(task=task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=task.at_a_stretch)))
						current_time = current_time + timezone.timedelta(minutes=task.at_a_stretch)
					else:
						# print("Hack 2")
						task.done = True
						done[task_index] = True
						schedule.append(Schedule(task=task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=task.left)))
						current_time = current_time + timezone.timedelta(minutes=task.left)
						task.left = 0
				else:
					if is_free_for > task.at_a_stretch:
						# print("Hack 3")
						task.left -= task.at_a_stretch
						schedule.append(Schedule(task=task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=task.at_a_stretch)))
						current_time = current_time + timezone.timedelta(minutes=task.at_a_stretch)
					else:
						# print("Hack 4")
						task.left -= is_free_for
						schedule.append(Schedule(task=task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=is_free_for)))
						current_time = current_time + timezone.timedelta(minutes=is_free_for)

			done_task_list[task_index] = task
			task_index += 1

	return schedule
