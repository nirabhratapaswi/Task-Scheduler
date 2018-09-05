from django.urls import path

from . import views

app_name = 'taskscheduler'
urlpatterns = [
    path('', views.prioritySchedule, name='prioritySchedule'),
    path('/createtask', views.createTask, name='createtask'),
]