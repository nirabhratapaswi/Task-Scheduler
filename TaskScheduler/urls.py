from django.urls import path

from . import views

app_name = 'taskscheduler'
urlpatterns = [
    path('', views.prioritySchedule, name='prioritySchedule'),
    path('/createtask', views.createTask, name='createtask'),
    path('/tasklist', views.getTasks, name='tasklist'),
    path('/schedule', views.schedule, name='schedule'),
    path('/deletetask', views.deleteTask, name='deletetask'),
]