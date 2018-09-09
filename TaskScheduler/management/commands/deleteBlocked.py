from django.core.management.base import BaseCommand, CommandError
from TaskScheduler.models import Blocked
from prompt_toolkit import prompt
from datetime import datetime
import pytz
# from prompt_toolkit.contrib.completers import WordCompleter

class Command(BaseCommand):
    help = 'Creates a new task to schedule'

    def add_arguments(self, parser):
        parser.add_argument('type', nargs='+', type=str)
        parser.add_argument('filter_value', nargs='+', type=str)
        print()

    def handle(self, *args, **options):
        for option in options["type"]:
            if option == "id":
                for blocked_id in options["filter_value"]:
                    b = Blocked.objects.get(pk=int(blocked_id))
                    delete = prompt("> Delete? (y-yes)")
                    if delete == "y" or delete == "Y":
                        print("Deleting blocked!")
                        b.delete()
            elif option == "name":
                for name in options["filter_value"]:
                    blocked = Blocked.objects.all().filter(name=name)
                    for b in blocked:
                        delete = prompt("> Delete"+b.name+", id: "+str(b.id)+"? (y-yes)")
                        if delete == "y" or delete == "Y":
                            print("Deleting blocked!")
                            b.delete()

        self.stdout.write(self.style.SUCCESS("Successfully deleted blocked"))