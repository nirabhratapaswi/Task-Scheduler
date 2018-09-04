from .models import Task, Schedule, Blocked
from django.utils import timezone

def roundToNearestHour(time, *args):
	time -= timezone.timedelta(minutes=time.minute, seconds=time.second)
	return time

def isFreeFor(currentTime, task, blocked_list, *args):	# blocked_list is sorted in ascending order
	is_free_for = 0
	blocked_till = currentTime
	if len(blocked_list) == 0:
		print("Flag 5.0")
		is_free_for = task.span
		blocked_till = currentTime+timezone.timedelta(minutes=task.span)
		return [is_free_for, blocked_till]
	if currentTime < blocked_list[0].start_time:
		print("Flag 5.1")
		is_free_for = (blocked_list[0].start_time - currentTime).total_seconds()/60
		blocked_till = None
		return [is_free_for, blocked_till]

	for i in range(0, len(blocked_list)-1):
		if currentTime >= blocked_list[i].end_time and currentTime < blocked_list[i+1].start_time:
			print("Flag 5.2")
			is_free_for = (blocked_list[i+1].start_time - blocked_list[i].end_time).total_seconds()/60
			blocked_till = None
			break
		if currentTime >= blocked_list[i].start_time and currentTime < blocked_list[i].end_time:
			print("Flag 5.3")
			is_free_for = 0
			blocked_till = blocked_list[i].end_time
			break

	if currentTime >= blocked_list[len(blocked_list)-1].end_time:
		print("Flag 5.4")
		is_free_for = task.span
		blocked_till = currentTime+timezone.timedelta(minutes=task.span)
		return [is_free_for, blocked_till]
	elif currentTime >= blocked_list[len(blocked_list)-1].start_time and currentTime < blocked_list[len(blocked_list)-1].end_time:
		print("Flag 5.5")
		is_free_for = 0
		blocked_till = blocked_list[len(blocked_list)-1].end_time

	return [is_free_for, blocked_till]

def scheduleTasks(task_list, blocked_list, *args):	# task_list is assumed to be Sorted sequentially by some logic, blocked_list is sorted in ascending order
	schedule = list()
	checkDelta = timezone.timedelta(minutes=30)	# schedule only in intervals of 30 minutes
	currentTime = timezone.now()
	currentTime = roundToNearestHour(currentTime)
	done = [False for x in range(0, len(task_list))]
	j = 0
	done_task_list = [None]*len(task_list)
	while False in done:
		print(done)
		i = 0
		if j > 50:
			break
		task_index = 0
		for task in task_list:
			if not done[task_index]:
				print("For task: " + task.task_name)
				[is_free_for, blocked_till] = isFreeFor(currentTime, task, blocked_list)
				print("is_free_for: " + str(is_free_for) + ", blocked_till: " + str(blocked_till))
				k = 0
				while is_free_for == 0:
					if k > 100:
						break
					currentTime = blocked_till
					[is_free_for, blocked_till] = isFreeFor(currentTime, task, blocked_list)
					print("is_free_for: " + str(is_free_for) + ", blocked_till: " + str(blocked_till))
					k += 1

				if is_free_for >= task.left:
					if task.left > task.at_a_stretch:
						print("Hack 1")
						task.left -= task.at_a_stretch
						schedule.append(Schedule(task=task, start_time=currentTime, end_time=currentTime+timezone.timedelta(minutes=task.at_a_stretch)))
						currentTime = currentTime+timezone.timedelta(minutes=task.at_a_stretch)
					else:
						print("Hack 2")
						task.done = True
						done[task_index] = True
						schedule.append(Schedule(task=task, start_time=currentTime, end_time=currentTime+timezone.timedelta(minutes=task.left)))
						currentTime = currentTime+timezone.timedelta(minutes=task.left)
						task.left = 0
				else:
					print("Hack 3")
					task.left -= is_free_for
					schedule.append(Schedule(task=task, start_time=currentTime, end_time=currentTime+timezone.timedelta(minutes=is_free_for)))
					currentTime = currentTime+timezone.timedelta(minutes=is_free_for)

			done_task_list[task_index] = task
			task_index += 1
		i += 1
		j += 1

	return schedule
