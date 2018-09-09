from django.core.management.base import BaseCommand, CommandError
from TaskScheduler.models import Schedule
from prompt_toolkit import prompt
from TaskScheduler import CRUD as crud
# from TaskScheduler import Slack as scAlgo
from django.utils import timezone
from terminaltables import AsciiTable
from TaskScheduler import SlackRoundRobinScheduler as SRRS

class Command(BaseCommand):
    help = 'Creates a new task to schedule'

    def add_arguments(self, parser):
        # parser.add_argument('new_task', nargs='+', type=int)
        print()

    def handle(self, *args, **options):
        # for task in options['new_task']:
        now = SRRS.roundToNearestHour(timezone.now())
        tasks = crud.readUndoneTasks()
        blocked = crud.readBlocked(now)
        taskList = list()
        for t in tasks:
            taskList.append(t)

        blockedList = list()
        for b in blocked:
            blockedList.append(b)

        current_time = now
        schedule = SRRS.scheduleTasks(taskList, current_time, blockedList)
        
        table_data = [
            ["id", "Task Name", "Start Time(yyyy-mm-dd HH:MM:SS)", "End Time(yyyy-mm-dd HH:MM:SS)", "Duration (minutes)"]
        ]
        for s in schedule:
            table_data.append([
                str(s.id), s.task.name, str(s.start_time), str(s.end_time), str((s.end_time - s.start_time).total_seconds()/60)
            ])

        table = AsciiTable(table_data)
        table.title = "Schedule"
        print (table.table)

        self.stdout.write(self.style.SUCCESS("Successfully saved task"))