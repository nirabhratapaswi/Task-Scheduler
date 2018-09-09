from django.core.management.base import BaseCommand, CommandError
from TaskScheduler.models import Task
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
                    ["id", "Task Name", "Priority", "Deadline(yyyy-mm-dd HH:MM:SS)", "Span", "Left", "Done"]
                ]
                for t in Task.objects.all().order_by("deadline"):
                    # print("Task Name: " + t.name + ", Span: " + str(t.span) + ", Deadline: " + str(t.deadline), ", Priority: ", str(t.priority) + ", Done; " + str(t.done))
                    table_data.append([
                        str(t.id), t.name, str(t.span), str(t.deadline), str(t.priority), str(t.left), str(t.done)
                    ])

                table = AsciiTable(table_data)
                table.title = "All Tasks"
                print (table.table)
            elif opt == "undone":
                table_data = [
                    ["id", "Task Name", "Priority", "Deadline(yyyy-mm-dd HH:MM:SS)", "Span", "Left", "Done"]
                ]
                for t in Task.objects.all().filter(done=False):
                    # print("Task Name: " + t.name + ", Span: " + str(t.span) + ", Deadline: " + str(t.deadline), ", Priority: ", str(t.priority) + ", Done; " + str(t.done))
                    table_data.append([
                        str(t.id), t.name, str(t.span), str(t.deadline), str(t.priority), str(t.left), str(t.done)
                    ])

                table = AsciiTable(table_data)
                table.title = "Undone Tasks"
                print (table.table)
            elif opt == "done":
                table_data = [
                    ["id", "Task Name", "Priority", "Deadline(yyyy-mm-dd HH:MM:SS)", "Span", "Left", "Done"]
                ]
                for t in Task.objects.all().filter(done=True):
                    # print("Task Name: " + t.name + ", Span: " + str(t.span) + ", Deadline: " + str(t.deadline), ", Priority: ", str(t.priority) + ", Done; " + str(t.done))
                    table_data.append([
                        str(t.id), t.name, str(t.span), str(t.deadline), str(t.priority), str(t.left), str(t.done)
                    ])

                table = AsciiTable(table_data)
                table.title = "Done Tasks"
                print (table.table)
            elif opt == "priority":
                table_data = [
                    ["id", "Task Name", "Priority", "Deadline(yyyy-mm-dd HH:MM:SS)", "Span", "Left", "Done"]
                ]
                for t in Task.objects.all().order_by("-priority"):
                    # print("Task Name: " + t.name + ", Span: " + str(t.span) + ", Deadline: " + str(t.deadline), ", Priority: ", str(t.priority) + ", Done; " + str(t.done))
                    table_data.append([
                        str(t.id), t.name, str(t.span), str(t.deadline), str(t.priority), str(t.left), str(t.done)
                    ])

                table = AsciiTable(table_data)
                table.title = "Priority Sorted Tasks"
                print (table.table)
            elif opt == "deadlineover":
                table_data = [
                    ["id", "Task Name", "Priority", "Deadline(yyyy-mm-dd HH:MM:SS)", "Span", "Left", "Done"]
                ]
                now = timezone.now()
                print("Time now: " + str(now))
                for t in Task.objects.all().filter(deadline__lt=now).order_by('deadline'):
                    # print("Task Name: " + t.name + ", Span: " + str(t.span) + ", Deadline: " + str(t.deadline), ", Priority: ", str(t.priority) + ", Done; " + str(t.done))
                    table_data.append([
                        str(t.id), t.name, str(t.span), str(t.deadline), str(t.priority), str(t.left), str(t.done)
                    ])

                table = AsciiTable(table_data)
                table.title = "Priority Sorted Tasks"
                print (table.table)
            else:
                print("Passed variable didn't match any pattern. Options available: all, done, undone, priority, deadlineover")

        self.stdout.write(self.style.SUCCESS("Successfully displayed task list"))