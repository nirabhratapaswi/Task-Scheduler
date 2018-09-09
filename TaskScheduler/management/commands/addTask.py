from django.core.management.base import BaseCommand, CommandError
from TaskScheduler.models import Task
from prompt_toolkit import prompt
from datetime import datetime
import pytz
# from prompt_toolkit.contrib.completers import WordCompleter

class Command(BaseCommand):
    help = 'Creates a new task to schedule'

    def add_arguments(self, parser):
        # parser.add_argument('new_task', nargs='+', type=int)
        print()

    def handle(self, *args, **options):
        # for task in options['new_task']:
        try:
            self.params = ["name", "deadline", "span", "at_a_stretch"]
            t = Task()
            t.name = prompt("* Enter Task Name: ")
            t.span = prompt("* Enter Task Span: ")
            t.left = t.span
            t.priority = prompt("* Enter Task Priority (0-low, 1-medium, 2-high): ")
            t.deadline = pytz.utc.localize(datetime.strptime(prompt("* Enter Task Deadline (format- mm/dd/yyyy HH:MM:SS): "), "%m/%d/%Y %H:%M:%S")) # to convert datetime native object to django timezone type
            t.done = False
            print("Task Name: " + t.name + ", Span: " + str(t.span) + ", Deadline: " + str(t.deadline), ", Priority: ", str(t.priority))
            save = prompt("> Save? (y-yes)")
            if save == "y" or save == "Y":
                print("Saving task!")
                t.save()
        except Task.DoesNotExist:
            raise CommandError('Task does not exist')

        self.stdout.write(self.style.SUCCESS("Successfully saved task"))