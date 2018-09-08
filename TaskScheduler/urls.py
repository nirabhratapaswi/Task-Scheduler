from django.urls import path

from . import views

app_name = 'taskscheduler'
urlpatterns = [
    # path('', views.prioritySchedule, name='prioritySchedule'),
    path('/schedule', views.schedule, name='schedule'),
    path('/createtask', views.createTask, name='createtask'),
    path('/tasklist', views.getTasks, name='tasklist'),
    path('/deletetask', views.deleteTask, name='deletetask'),
    path('/createblocked', views.createBlocked, name='createblocked'),
    path('/blockedlist', views.getBlocked, name='blockedlist'),
    path('/deleteblocked', views.deleteBlocked, name='deleteblocked'),
]