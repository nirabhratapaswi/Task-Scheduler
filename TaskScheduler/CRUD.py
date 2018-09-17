from .models import Task, Schedule, Blocked, WeeklySchedule, DaysRepeated

def createTask(name, priority, span, deadline, at_a_stretch, done, max_repeats_per_day, times_repeated_today, break_needed_afterwards, **kwargs):
	try:
		if "id" in kwargs:
			task = Task.objects.get(pk=kwargs["id"])
			task.name = name
			task.priority = priority
			task.deadline = deadline
			task.span = span
			task.left = span
			task.at_a_stretch = at_a_stretch
			task.done = done
			task.max_repeats_per_day = max_repeats_per_day
			task.times_repeated_today = times_repeated_today
			task.break_needed_afterwards = break_needed_afterwards
		else:
			task = Task(name=name, priority=priority, span=span, deadline=deadline, at_a_stretch=at_a_stretch, left=span, done=done, max_repeats_per_day=max_repeats_per_day, times_repeated_today=times_repeated_today, break_needed_afterwards=break_needed_afterwards)
		task.save()
		return [True, None]	# TODO: write condition for saving and logical failured
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def deleteTaskById(task_id, *args):
	try:
		task = Task.objects.get(pk=task_id)
		task.delete()
		return [True, None]
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def deleteTaskByName(name, *args):
	try:
		task = Task.objects.get(name=name)
		task.delete()
		return [True, None]
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def createBlocked(name, start_time, end_time, **kwargs):	# check if slot is already booked!
	try:
		if "id" in kwargs:
			blocked_tasks = Blocked.objects.filter(end_time__gt=start_time).filter(start_time__lt=end_time)
			weekly_schedule_tasks = DaysRepeated.objects.filter(day_index__in=[str(start_time.weekday()), str(end_time.weekday())]).filter(weekly_schedule__hard_bound=True).filter(weekly_schedule__end_time__gt=start_time.time()).filter(weekly_schedule__start_time__lt=end_time.time())
			if len(blocked_tasks) > 0 or len(weekly_schedule_tasks) > 0:
				return [False, "Time is already blocked by some other task -- check blocked tasks or hard bound weekly schedule"]
			blocked = Blocked.objects.get(pk=kwargs["id"])
			blocked.name = name
			blocked.start_time = start_time
			blocked.end_time = end_time
		else:
			blocked_tasks = Blocked.objects.filter(end_time__gt=start_time).filter(start_time__lt=end_time)
			weekly_schedule_tasks = DaysRepeated.objects.filter(day_index__in=[str(start_time.weekday()), str(end_time.weekday())]).filter(weekly_schedule__hard_bound=True).filter(weekly_schedule__end_time__gt=start_time.time()).filter(weekly_schedule__start_time__lt=end_time.time())
			if len(blocked_tasks) > 0 or len(weekly_schedule_tasks) > 0:
				return [False, "Time is already blocked by some other task -- check blocked tasks or hard bound weekly schedule"]
			blocked = Blocked(name=name, start_time=start_time, end_time=end_time)
		blocked.save()
		return [True, None]	# TODO: write condition for saving and logical failured
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def deleteBlockedById(blocked_id, *args):
	try:
		blocked = Blocked.objects.get(pk=blocked_id)
		blocked.delete()
		return [True, None]
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def deleteBlockedByName(name, *args):
	try:
		blocked = Blocked.objects.get(name=name)
		blocked.delete()
		return [True, None]
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def createWeeklySchedule(name, start_time, end_time, days_repeated, minimum_time_to_devote, hard_bound, **kwargs):	# check if slot is already booked!
	try:
		if "id" in kwargs:
			if hard_bound:
				blocked_tasks = Blocked.objects.all()
				blocked_tasks_list = list()
				for b in blocked_tasks:
					if b.start_time.time() < end_time and b.end_time.time() > start_time:
						blocked_tasks_list.append(b)
				# weekly_schedule_tasks = WeeklySchedule.objects.filter(hard_bound=True).filter(end_time__gt=start_time).filter(start_time__lt=end_time)
				weekly_schedule_tasks = DaysRepeated.objects.filter(day_index__in=days_repeated).filter(weekly_schedule__hard_bound=True).filter(weekly_schedule__end_time__gt=start_time).filter(weekly_schedule__start_time__lt=end_time)
				if len(blocked_tasks_list) > 0 or len(weekly_schedule_tasks) > 0:
					return [False, "Time is already blocked by some other task -- check blocked tasks or hard bound weekly schedule"]
			weekly_schedule = WeeklySchedule.objects.get(pk=kwargs["id"])
			weekly_schedule.name = name
			weekly_schedule.start_time = start_time
			weekly_schedule.end_time = end_time
			weekly_schedule.minimum_time_to_devote = minimum_time_to_devote
			weekly_schedule.hard_bound = hard_bound
			weekly_schedule.save()
		else:
			if hard_bound:
				blocked_tasks = Blocked.objects.all()
				blocked_tasks_list = list()
				for b in blocked_tasks:
					if b.start_time.time() < end_time and b.end_time.time() > start_time:
						blocked_tasks_list.append(b)
				# weekly_schedule_tasks = WeeklySchedule.objects.filter(hard_bound=True).filter(end_time__gt=start_time).filter(start_time__lt=end_time)
				weekly_schedule_tasks = DaysRepeated.objects.filter(day_index__in=days_repeated).filter(weekly_schedule__hard_bound=True).filter(weekly_schedule__end_time__gt=start_time).filter(weekly_schedule__start_time__lt=end_time)
				if len(blocked_tasks_list) > 0 or len(weekly_schedule_tasks) > 0:
					return [False, "Time is already blocked by some other task -- check blocked tasks or hard bound weekly schedule"]
			weekly_schedule = WeeklySchedule(name=name, start_time=start_time, end_time=end_time, minimum_time_to_devote=minimum_time_to_devote, hard_bound=hard_bound)
			weekly_schedule.save()
			for d in days_repeated:
				days_repeated = DaysRepeated(weekly_schedule=weekly_schedule, day_index=d)
				days_repeated.save()
		return [True, None]	# TODO: write condition for saving and logical failured
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def deleteWeeklyScheduleById(weekly_schedule_id, *args):
	try:
		weekly_schedule = WeeklySchedule.objects.get(pk=weekly_schedule_id)
		weekly_schedule.delete()
		return [True, None]
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def createDaysRepeated(weekly_schedule, day_index, *args):
	try:
		days_repeated = DaysRepeated(weekly_schedule=weekly_schedule, day_index=day_index)
		days_repeated.save()
		return [True, None]	# TODO: write condition for saving and logical failured
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def deleteDaysRepeatedById(days_repeated_id, *args):
	try:
		days_repeated =	DaysRepeated.objects.get(pk=days_repeated_id)
		days_repeated.delete()
		return [True, None]
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def saveSchedule(schedule_list, *args):
	try:
		for s in schedule_list:
			s.save()
		return [True, None]
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

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
		blocked = Blocked.objects.filter(end_time__gt=args[0]).order_by('start_time')
	else:	
		blocked = Blocked.objects.all().order_by('start_time')
	return blocked

def readWeeklySchedule(*args):
	weekly_schedule = WeeklySchedule.objects.all()
	return weekly_schedule

def readScheduleList(*args):
	schedule_list = list()
	for s in Schedule.objects.all().order_by('start_time'):
		schedule_list.append(s)

	return schedule_list

def getWeeklySchedulePerDayAsList(*args):
	weekly_schedule = list()
	for day in range(0, 7):
		weekly_schedule.append(DaysRepeated.objects.filter(day_index=day).order_by('weekly_schedule__start_time'))

	return weekly_schedule

# Scheduling CRUDs
def updateScheduleStatus(schedule_id, current_time, done_status, **kwargs):
	try:
		schedule = Schedule.objects.filter(pk=schedule_id).filter(start_time__lte=current_time)
		if len(schedule) == 0:
			return [False, "Task in the Future cannot be marked as undone!"]
		else:
			for s in schedule:
				s.done = done_status
				s.save()
			return [True, None]
	except Exception as e:
		return [False, str(e.message)+str(type(e))]

def readSchedule(*args):
	schedule = list()
	for s in Schedule.objects.all():
		schedule.append(s)
	return schedule

def readPastSchedulesAsList(current_time, *args):
	schedule = list()
	for s in Schedule.objects.filter(start_time__lte=current_time):
		schedule.append(s)
	Schedule.objects.filter(start_time__gt=current_time).delete()
	return schedule