##
#	have check for tasks with impossible deadlines, or bunch of tasks together constituting impossible deadlines,
#	so that infinite loop is not triggered while scheduling
##

from .models import Task, Schedule, Blocked
from django.utils import timezone
from datetime import datetime, date, time
import pytz

def roundToNearestHour(time, *args):
	if time.minute > 0 and time.minute <= 30:
		time -= timezone.timedelta(minutes=time.minute, seconds=time.second)
		time = time.replace(minute=30, microsecond=0)
	else:
		time -= timezone.timedelta(hours=-1, minutes=time.minute, seconds=time.second)
		time = time.replace(minute=0, microsecond=0)
	return time

def alphabeticalSortFunctionWrtName(task):
	return task.name

def dateSortFunctionWrtPriority(task):
	return task.priority

def dateSortFunctionWrtDeadline(task):
	return task.deadline

def findSlackTime(task, blocked_list, current_time, *args):
	# print("For Slack Time, blocked_list: ")
	# for b in blocked_list:
	# 	print("Blocked Name:" + b.name + ", start_time" + str(b.start_time) + ", end_time: " + str(b.end_time))
	slack_task = None
	available_time_till_deadline = (task.deadline - current_time).total_seconds()/60
	# print("Task deadline: " + str(task.deadline) + ", available_time_initial: " + str(available_time_till_deadline))
	for b in blocked_list:
		if b.start_time >= current_time and b.end_time <= task.deadline:
			# print("Condition 0, name: " + b.name, ", substration: " + str((b.end_time - b.start_time).total_seconds()/60))
			available_time_till_deadline -= (b.end_time - b.start_time).total_seconds()/60
		elif b.start_time <= task.deadline and b.end_time > task.deadline:
			# print("Condition 1, name: " + b.name, ", substration: " + str((task.deadline - b.start_time).total_seconds()/60))
			available_time_till_deadline -= (task.deadline - b.start_time).total_seconds()/60

	return available_time_till_deadline - task.left

def timeQuantumSummation(task_list, priority, *args):
	tq_sum = 0
	for t in task_list:
		# if priority <= t.priority:	# modify to reschedule deadline approaching tasks
		tq_sum += t.at_a_stretch

	# print("timeQuantumSummation: " + str(tq_sum))
	return tq_sum

def removeBlockedTask(current_time, blocked_list, *args):
	while(len(blocked_list) > 0 and blocked_list[0].end_time <= current_time):
		blocked_list.pop(0)
	return blocked_list

def removeDoneTasks(task_list, done_task_list, *args):	# Note, this only removes on the basis of time left to do the task, because task.done is True only when user confirms the tasks are done in real time!
	left_task_list = list()
	for t in task_list:
		if t.left > 0:
			left_task_list.append(t)
		else:
			done_task_list.append(t)

	return [left_task_list, done_task_list]

def filterHardSoftBoundWeeklyTasks(daily_schedule, *args):
	hard_bound_schedule = list()
	soft_bound_schedule = list()
	for task in daily_schedule:
		if task.weekly_schedule.hard_bound:
			hard_bound_schedule.append(task)
		else:
			soft_bound_schedule.append(task)

	return [hard_bound_schedule, soft_bound_schedule]

def addWeekdayScheduleToBlockedList(current_time, blocked_list, weekly_schedule_list, increment_day, *args):
	new_blocked_list = list()
	[hard_bound_schedule, soft_bound_schedule] = filterHardSoftBoundWeeklyTasks(weekly_schedule_list[(current_time.weekday()+increment_day)%7])
	# hard_bound_schedule = weekly_schedule_list[(current_time.weekday()+increment_day)%7]
	for schedule in hard_bound_schedule:
		if increment_day == 0 and current_time.time() >= schedule.weekly_schedule.start_time and current_time.time() < schedule.weekly_schedule.end_time:
			start_time = current_time + timezone.timedelta(days=increment_day)
			end_time = datetime.combine(date(current_time.year, current_time.month, current_time.day), schedule.weekly_schedule.end_time).replace(tzinfo=pytz.UTC) + timezone.timedelta(days=increment_day)
		elif current_time.time() < schedule.weekly_schedule.start_time or increment_day == 1:
			start_time = datetime.combine(date(current_time.year, current_time.month, current_time.day), schedule.weekly_schedule.start_time).replace(tzinfo=pytz.UTC) + timezone.timedelta(days=increment_day)
			end_time = datetime.combine(date(current_time.year, current_time.month, current_time.day), schedule.weekly_schedule.end_time).replace(tzinfo=pytz.UTC) + timezone.timedelta(days=increment_day)
		else:
			continue
		blocked_instance = Blocked(name=schedule.weekly_schedule.name, start_time=start_time, end_time=end_time)
		schedule_added = False
		while not schedule_added:
			if len(blocked_list) > 0 and blocked_instance.start_time < blocked_list[0].start_time:
				# print("Flag 0")
				new_blocked_list.append(blocked_instance)
				schedule_added = True
			elif len(blocked_list)==0:
				# print("Flag 1")
				new_blocked_list.append(blocked_instance)
				schedule_added = True
			else:
				# print("Flag 2")
				new_blocked_list.append(blocked_list[0])
				blocked_list.pop(0)

	for blocked in blocked_list:
		new_blocked_list.append(blocked)
	return new_blocked_list

def completeDeadlineApproachingTask(current_time, task, blocked_list, schedule, *args):
	while task.left > 0:
		if len(blocked_list) > 0:
			if current_time < blocked_list[0].start_time:
				if blocked_list[0].start_time - current_time >= timezone.timedelta(minutes=task.left):
					# print("Appending Schedule at 1")
					schedule.append(Schedule(task=task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=task.left)))
					current_time += timezone.timedelta(minutes=task.left)
					task.left = 0
					task.done = True
					# task.save()
				else:
					# print("Appending Schedule at 2")
					schedule.append(Schedule(task=task, start_time=current_time, end_time=blocked_list[0].start_time))
					task.left -= (blocked_list[0].start_time - current_time).total_seconds()/60
					current_time = blocked_list[0].end_time
					blocked_list = removeBlockedTask(current_time, blocked_list)
			else:
				current_time = blocked_list[0].end_time
				blocked_list = removeBlockedTask(current_time, blocked_list)
		else:
			# print("Appending Schedule at 3")
			schedule.append(Schedule(task=task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=task.left)))
			current_time += timezone.timedelta(minutes=task.left)
			task.left = 0
			task.done = True
			# task.save()
	current_time += timezone.timedelta(minutes=task.break_needed_afterwards)
	return [current_time, schedule, blocked_list]

def scheduleTaskNormally(current_time, task, blocked_list, schedule, time_quantum, *args):
	while time_quantum>0:
		if len(blocked_list) > 0:
			if current_time < blocked_list[0].start_time:
				if (blocked_list[0].start_time - current_time) >= timezone.timedelta(minutes=time_quantum):
					# print("Appending Schedule at 4")
					schedule.append(Schedule(task=task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=time_quantum)))
					current_time += timezone.timedelta(minutes=time_quantum)
					time_quantum = 0
					# task.done = True
					# task.save()
				else:
					# print("Appending Schedule at 5")
					schedule.append(Schedule(task=task, start_time=current_time, end_time=blocked_list[0].start_time))
					time_quantum -= (blocked_list[0].start_time - current_time).total_seconds()/60
					current_time = blocked_list[0].end_time
					blocked_list = removeBlockedTask(current_time, blocked_list)
			else:
				current_time = blocked_list[0].end_time
				blocked_list = removeBlockedTask(current_time, blocked_list)
		else:
			# print("Appending Schedule at 6")
			schedule.append(Schedule(task=task, start_time=current_time, end_time=current_time+timezone.timedelta(minutes=time_quantum)))
			current_time += timezone.timedelta(minutes=time_quantum)
			time_quantum = 0
			# task.done = True
			# task.save()
	current_time += timezone.timedelta(minutes=task.break_needed_afterwards)
	return [current_time, schedule]

def filterRepetitionsOverTasks(task_list, *args):
	todays_task_list = list()
	todays_task_list_index = list()
	done_repeating_today = list()
	done_repeating_today_index = list()
	index = 0
	for task in task_list:
		if task.times_repeated_today >= task.max_repeats_per_day:
			done_repeating_today.append(task)
			done_repeating_today_index.append(index)
		else:
			todays_task_list.append(task)
			todays_task_list_index.append(index)
		index += 1

	return [todays_task_list, todays_task_list_index, done_repeating_today, done_repeating_today_index]

def renewTimesRepeatedToday(task_list, *args):
	index = 0
	for task in task_list:
		task.times_repeated_today = 0
		task_list[index] = task
		index += 1
	
	return task_list

def checkForNextDay(current_date, current_time, task_list, blocked_list, weekly_schedule_list, *args):
	if current_date != current_time.date() + timezone.timedelta(days=1):
		blocked_list = addWeekdayScheduleToBlockedList(current_time, blocked_list, weekly_schedule_list, 1)
		current_date = current_time.date() + timezone.timedelta(days=1)
		task_list = renewTimesRepeatedToday(task_list)

	return [current_date, task_list, blocked_list]

def scheduleSoftBoundWeeklyTasks(current_time, task_list, weekly_schedule_list, schedule, add_all, *args):
	if not add_all:
		[hard_bound_schedule, soft_bound_schedule] = filterHardSoftBoundWeeklyTasks(weekly_schedule_list[current_time.weekday()%7])
		for task in soft_bound_schedule:
			if current_time.time() >= task.weekly_schedule.start_time and current_time.time() < task.weekly_schedule.end_time:
				end_time = datetime.combine(date(current_time.year, current_time.month, current_time.day), task.weekly_schedule.end_time).replace(tzinfo=pytz.UTC)
				# schedule.append(Schedule(task=task, start_time=current_time, end_time=end_time))
				current_time = end_time

		return [current_time, schedule]
	else:
		midnight = datetime.combine(date(current_time.year, current_time.month, current_time.day), time(0, 0, 0, 0)).replace(tzinfo=pytz.UTC) + timezone.timedelta(days=1)	# Not needed, as time cant exceed 00:00
		[hard_bound_schedule, soft_bound_schedule] = filterHardSoftBoundWeeklyTasks(weekly_schedule_list[current_time.weekday()%7])
		for task in soft_bound_schedule:
			if current_time.time() <= task.weekly_schedule.start_time and current_time < midnight:
				end_time = datetime.combine(date(current_time.year, current_time.month, current_time.day), task.weekly_schedule.end_time).replace(tzinfo=pytz.UTC)
				# schedule.append(Schedule(task=task, start_time=task.start_time, end_time=end_time))
				current_time = end_time

		return [current_time, schedule]

def scheduleTasks(task_list, current_time, blocked_list, weekly_schedule_list, *args):	# assuming blocked list and weekly_schedule_list is sorted in ascending order, and there are no time conflicts between them
	if len(task_list)==0:
		return None;
	for s in Schedule.objects.all():	# Comment out later when integration with scheduling database is done.
		s.delete()
	START_TIME = datetime.now()
	print("START_TIME: " + str(START_TIME))
	schedule = list()
	done_task_list = list()
	# current_time = roundToNearestHour(current_time)	# check necessity if already called from parent function
	blocked_list = addWeekdayScheduleToBlockedList(current_time, blocked_list, weekly_schedule_list, 0)
	blocked_list = addWeekdayScheduleToBlockedList(current_time, blocked_list, weekly_schedule_list, 1)
	current_date = current_time.date() + timezone.timedelta(days=1)
	while len(task_list) > 0:
		[current_date, task_list, blocked_list] = checkForNextDay(current_date, current_time, task_list, blocked_list, weekly_schedule_list)
		blocked_list = removeBlockedTask(current_time, blocked_list)	# check if this call is absolutely necessary
		# task_list.sort(key=dateSortFunctionWrtDeadline)
		unsafe_deadline = False
		index = 0
		for task in task_list:	# Check for any deadline approaching tasks
			slack_check_task = task_list.pop(index)
			slack_time = findSlackTime(slack_check_task, blocked_list, current_time)
			print("For task: " + slack_check_task.name + ", slack_time: " + str(slack_time))
			# task_list.sort(key=alphabeticalSortFunctionWrtName)
			# task_list.sort(key=dateSortFunctionWrtPriority, reverse=True)	# for timeQuantumSummation to calculate time sum of only higher priorities
			if (slack_time < timeQuantumSummation(task_list, slack_check_task.priority)):
				[current_time, schedule, blocked_list] = completeDeadlineApproachingTask(current_time, slack_check_task, blocked_list, schedule)
				unsafe_deadline = True
				break
			else:
				task_list.insert(index, slack_check_task)
			index += 1

		if unsafe_deadline:
			continue
		else:
			# task_list.insert(0, slack_check_task)	# if slack validity holds good, reinsert the task at inspection
			task_list.sort(key=dateSortFunctionWrtPriority, reverse=True)
			# Complete 1 cycle of round robin
			if len(task_list) == 1:	# write seperate logic, combine the task to one
				# for t in task_list:	# Note: Maintain the time quantum amount of task assignment! -> important for consistancy
				task = task_list[0]
				time_quantum = task.left
				[current_time, schedule] = scheduleTaskNormally(current_time, task, blocked_list, schedule, time_quantum)
				task.left = 0
				task.times_repeated_today += 1
				# task.done = True
				task_list[0] = task
			else:
				[todays_task_list, todays_task_list_index, done_repeating_today, done_repeating_today_index] = filterRepetitionsOverTasks(task_list)
				index = 0
				if len(todays_task_list) == 0:
					# Check if done_repeating_today tasks have deadline approaching if stated tomorrow?
					saved_current_time = current_time
					current_time = datetime.combine(date(current_time.year, current_time.month, current_time.day), time(0, 0, 0, 0)).replace(tzinfo=pytz.UTC) + timezone.timedelta(days=1)	# Go to next day!
					index = 0
					for task in done_repeating_today:
						slack_time = findSlackTime(task, blocked_list, current_time)
						done_repeating_today.pop(index)	# take out task with earliest deadline to check slack validity -> commented to avoid check after task sort
						if (slack_time < timeQuantumSummation(done_repeating_today, task.priority)):
							[saved_current_time, schedule, blocked_list] = completeDeadlineApproachingTask(saved_current_time, task, blocked_list, schedule)
							task_list[done_repeating_today_index[index]].left = 0
						index += 1
						# [current_time, schedule] = scheduleSoftBoundWeeklyTasks(current_time, task_list, weekly_schedule_list, schedule, True)
						[current_date, task_list, blocked_list] = checkForNextDay(current_date, current_time, task_list, blocked_list, weekly_schedule_list)
				else:
					for task in todays_task_list:	# Note: Maintain the time quantum amount of task assignment! -> important for consistancy
						# current_time_save = current_time
						# [current_time, schedule] = scheduleSoftBoundWeeklyTasks(current_time, task_list, weekly_schedule_list, schedule, False)
						# deadline_breached = False
						# deadline_index = 0
						# for t in task_list:	# Check for any deadline approaching tasks
						# 	slack_check_task = task_list.pop(deadline_index)
						# 	slack_time = findSlackTime(slack_check_task, blocked_list, current_time)
						# 	if (slack_time < timeQuantumSummation(task_list, slack_check_task.priority)):
						# 		[current_time, schedule, blocked_list] = completeDeadlineApproachingTask(current_time, slack_check_task, blocked_list, schedule)
						# 		deadline_breached = True
						# 	task_list.insert(deadline_index, slack_check_task)
						# 	deadline_index += 1
						# if deadline_breached:
						# 	current_time = current_time_save
						# 	schedule.pop()
						time_quantum = task.at_a_stretch
						[current_time, schedule] = scheduleTaskNormally(current_time, task, blocked_list, schedule, time_quantum)
						task.left -= task.at_a_stretch
						task.times_repeated_today += 1
						task_list[todays_task_list_index[index]] = task
						index += 1
						[current_date, task_list, blocked_list] = checkForNextDay(current_date, current_time, task_list, blocked_list, weekly_schedule_list)
		[task_list, done_task_list] = removeDoneTasks(task_list, done_task_list)	# to remove Done Tasks

	for s in schedule:
		s.save()
	END_TIME = datetime.now()
	print("END_TIME: " + str(END_TIME))
	print("Time difference(seconds): " + str((END_TIME - START_TIME).total_seconds()))
	return schedule
