from django.core.management.base import BaseCommand, CommandError
from TaskScheduler.models import Blocked
from django.utils import timezone
from terminaltables import AsciiTable
# from prompt_toolkit.contrib.completers import WordCompleter

class Command(BaseCommand):
    help = 'Creates a new task to schedule'

    def add_arguments(self, parser):
        parser.add_argument('option', nargs='+', type=str)
        print()

    def handle(self, *args, **options):
        for opt in options['option']:
            if opt == "all":
                table_data = [
                    ["id", "Blocked Name", "Start Time", "End Time", "Span"]
                ]
                for b in Blocked.objects.all().order_by("start_time"):
                    # print("Blocked Name: " + t.name + ", Span: " + str(t.span) + ", Deadline: " + str(t.deadline), ", Priority: ", str(t.priority) + ", Done; " + str(t.done))
                    table_data.append([
                        str(b.id), b.name, str(b.start_time), str(b.end_time), str(b.end_time - b.start_time)
                    ])

                table = AsciiTable(table_data)
                table.title = "All Blocked"
                print (table.table)
            elif opt == "left":
                table_data = [
                    ["id", "Blocked Name", "Start Time", "End Time", "Span"]
                ]
                now = timezone.now()
                print("Time now: " + str(now))
                for b in Blocked.objects.all().filter(end_time__gt=now):
                    # print("Blocked Name: " + t.name + ", Span: " + str(t.span) + ", Deadline: " + str(t.deadline), ", Priority: ", str(t.priority) + ", Done; " + str(t.done))
                    table_data.append([
                        str(b.id), b.name, str(b.start_time), str(b.end_time), str(b.end_time - b.start_time)
                    ])

                table = AsciiTable(table_data)
                table.title = "Left Blocked"
                print (table.table)
            else:
                print("Passed variable didn't match any pattern. Options available: all, left")

        self.stdout.write(self.style.SUCCESS("Successfully displayed task list"))