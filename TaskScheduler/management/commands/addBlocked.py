from django.core.management.base import BaseCommand, CommandError
from TaskScheduler.models import Blocked
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
            self.params = ["name", "start_time", "end_time"]
            b = Blocked()
            b.name = prompt("* Enter Blocked Name: ")
            b.start_time = pytz.utc.localize(datetime.strptime(prompt("* Enter Blocked Start Time (format- mm/dd/yyyy HH:MM:SS): "), "%m/%d/%Y %H:%M:%S")) # to convert datetime native object to django timezone type
            b.end_time = pytz.utc.localize(datetime.strptime(prompt("* Enter Blocked End Time (format- mm/dd/yyyy HH:MM:SS): "), "%m/%d/%Y %H:%M:%S")) # to convert datetime native object to django timezone type
            print("Blocked Name: " + b.name + ", Start Time: " + str(b.start_time) + ", End Time: " + str(b.end_time))
            save = prompt("> Save? (y-yes)")
            if save == "y" or save == "Y":
                print("Saving blocked!")
                b.save()
        except Task.DoesNotExist:
            raise CommandError('Task does not exist')

        self.stdout.write(self.style.SUCCESS("Successfully saved task"))