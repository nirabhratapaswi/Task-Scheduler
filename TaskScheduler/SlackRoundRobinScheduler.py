##
#	have check for tasks with impossible deadlines, or bunch of tasks together constituting impossible deadlines,
#	so that infinite loop is not triggered while scheduling
##

from .models import Task, Schedule, Blocked
from django.utils import timezone

def roundToNearestHour(time, *args):
	if time.minute > 0 and time.minute <= 30:
		time -= timezone.timedelta(minutes=time.minute, seconds=time.second)
		time = time.replace(minute=30, microsecond=0)
	else:
		time -= timezone.timedelta(hours=-1, minutes=time.minute, seconds=time.second)
		time = time.replace(minute=0, microsecond=0)
	return time

def dateSortFunctionWrtPriority(task):
	return task.priority

def dateSortFunctionWrtDeadline(task):
	return task.deadline

def findSlackTime(task, blocked_list, current_time, *args):
	slack_task = None
	available_time_till_deadline = (task.deadline - current_time).total_seconds()/60
	for b in blocked_list:
		if b.start_time >= current_time and b.end_time <= task.deadline:
			available_time_till_deadline -= (b.end_time - b.start_time).total_seconds()/60
		elif b.start_time <= task.deadline and b.end_time > task.deadline:
			available_time_till_deadline -= (task.deadline - b.start_time).total_seconds()/60

	return available_time_till_deadline - task.left

def timeQuantumSummation(task_list, *args):
	tq_sum = 0
	for t in task_list:
		tq_sum += t.at_a_stretch

	return tq_sum

def removeBlockedTask(current_time, blocked_list, *args):
	while(len(blocked_list) > 0 and blocked_list[0].end_time <= current_time):
		blocked_list.pop(0)
	return blocked_list

def removeDoneTasks(task_list, done_task_list, *args):
	left_task_list = list()
	for t in task_list:
		if t.left > 0:
			left_task_list.append(t)
		else:
			done_task_list.append(t)

	return [left_task_list, done_task_list]

def scheduleTasks(task_list, current_time, blocked_list, *args):
	if len(task_list)==0:
		return None;
	schedule = list()
	done_task_list = list()
	# current_time = roundToNearestHour(current_time)	# check necessity if already called from parent function
	while len(task_list) > 0:
		# for s in schedule:
			# print("Task name: " + s.task.name + ", start: " + str(s.start_time) + ", end: " + str(s.end_time))
		blocked_list = removeBlockedTask(current_time, blocked_list)	# check if this call is absolutely necessary
		task_list.sort(key=dateSortFunctionWrtDeadline)
		slack_check_task = task_list[0]
		slack_time = findSlackTime(slack_check_task, blocked_list, current_time)
		task_list.pop(0)	# take out task with earliest deadline to check slack validity
		# print("For task: " + slack_check_task.name + ", slack_time: " + str(slack_time))
		if (slack_time < timeQuantumSummation(task_list)):
			while slack_check_task.left > 0:
				if len(blocked_list) > 0:
					if current_time < blocked_list[0].start_time:
						if blocked_list[0].start_time - current_time >= timezone.timedelta(minutes=slack_check_task.left):
							# print("Appending Schedule at 1")
							schedule.append(Schedule(task=slack_check_task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=slack_check_task.left)))
							current_time += timezone.timedelta(minutes=slack_check_task.left)
							slack_check_task.left = 0
						else:
							# print("Appending Schedule at 2")
							schedule.append(Schedule(task=slack_check_task, start_time=current_time, end_time=blocked_list[0].start_time))
							slack_check_task.left -= (blocked_list[0].start_time - current_time).total_seconds()/60
							current_time = blocked_list[0].end_time
							blocked_list = removeBlockedTask(current_time, blocked_list)
					else:
						current_time = blocked_list[0].end_time
						blocked_list = removeBlockedTask(current_time, blocked_list)
				else:
					# print("Appending Schedule at 3")
					schedule.append(Schedule(task=slack_check_task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=slack_check_task.left)))
					current_time += timezone.timedelta(minutes=slack_check_task.left)
					slack_check_task.left = 0
			continue
		else:
			task_list.insert(0, slack_check_task)	# if slack validity holds good, reinsert the task at inspection
			task_list.sort(key=dateSortFunctionWrtPriority, reverse=True)
			# Complete 1 cycle of round robin
			index = 0
			for t in task_list:	# Note: Maintain the time quantum amount of task assignment! -> important for consistancy
				time_quantum = t.at_a_stretch
				while time_quantum>0:
					if len(blocked_list) > 0:
						if current_time < blocked_list[0].start_time:
							if (blocked_list[0].start_time - current_time) >= timezone.timedelta(minutes=time_quantum):
								# print("Appending Schedule at 4")
								schedule.append(Schedule(task=t, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=time_quantum)))
								current_time += timezone.timedelta(minutes=time_quantum)
								time_quantum = 0
							else:
								# print("Appending Schedule at 5")
								schedule.append(Schedule(task=t, start_time=current_time, end_time=blocked_list[0].start_time))
								time_quantum -= (blocked_list[0].start_time - current_time).total_seconds()/60
								current_time = blocked_list[0].end_time
								blocked_list = removeBlockedTask(current_time, blocked_list)
						else:
							current_time = blocked_list[0].end_time
							blocked_list = removeBlockedTask(current_time, blocked_list)
					else:
						# print("Appending Schedule at 6")
						schedule.append(Schedule(task=t, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=time_quantum)))
						current_time += timezone.timedelta(minutes=time_quantum)
						time_quantum = 0
				t.left -= t.at_a_stretch
				task_list[index] = t
				index += 1

		[task_list, done_task_list] = removeDoneTasks(task_list, done_task_list)	# to remove Done Tasks

	return schedule
