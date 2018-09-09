from django.core.management.base import BaseCommand, CommandError
from TaskScheduler.models import Task
from prompt_toolkit import prompt
from datetime import datetime
import pytz
# from prompt_toolkit.contrib.completers import WordCompleter

class Command(BaseCommand):
    help = 'Deletes a new task'

    def add_arguments(self, parser):
        parser.add_argument('type', nargs='+', type=str)
        parser.add_argument('filter_value', nargs='+', type=str)
        print()

    def handle(self, *args, **options):
        for option in options["type"]:
            if option == "id":
                for task_id in options["filter_value"]:
                    t = Task.objects.get(pk=int(task_id))
                    delete = prompt("> Delete? (y-yes)")
                    if delete == "y" or delete == "Y":
                        print("Deleting task!")
                        t.delete()
            elif option == "name":
                for name in options["filter_value"]:
                    tasks = Task.objects.all().filter(name=name)
                    for t in tasks:
                        delete = prompt("> Delete"+t.name+", id: "+str(t.id)+"? (y-yes)")
                        if delete == "y" or delete == "Y":
                            print("Deleting task!")
                            t.delete()

        self.stdout.write(self.style.SUCCESS("Successfully deleted task"))