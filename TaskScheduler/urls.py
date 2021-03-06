from django.urls import path

from . import views

app_name = 'taskscheduler'
urlpatterns = [
    # path('', views.prioritySchedule, name='prioritySchedule'),
    path('schedule', views.viewSchedule, name='schedule'),
    path('prepareschedule', views.prepareSchedule, name='prepareschedule'),
    path('createtask', views.createTask, name='createtask'),
    path('tasklist', views.getTasks, name='tasklist'),
    path('deletetask', views.deleteTask, name='deletetask'),
    path('createblocked', views.createBlocked, name='createblocked'),
    path('blockedlist', views.getBlocked, name='blockedlist'),
    path('deleteblocked', views.deleteBlocked, name='deleteblocked'),
    path('createweeklyschedule', views.createWeeklySchedule, name='createweeklyschedule'),
    path('weeklyschedulelist', views.getWeeklySchedule, name='weeklyschedulelist'),
    path('deleteweeklyschedule', views.deleteWeeklySchedule, name='deleteweeklyschedule'),
    path('reportundonetaskasperschedule', views.reportUndoneTaskAsPerSchedule, name='reportundonetaskasperschedule'),
]