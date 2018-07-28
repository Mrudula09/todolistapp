from django.contrib import admin
from django.urls import path
from todoapp import views

from view.auth import *
from view.task import *

urlpatterns = [
    path('',loginView.as_view(),name='login_page'),
    path('logout/',logout_user,name='logout_page'),
    path('signup/',signupView.as_view(),name='signup_page'),
    path('tasklist/',TaskList.as_view(),name='task_list'),
    path('addTask/',AddTaskView.as_view(),name='add_task'),
    path('tasklist/<int:pk>/update',UpdateTask.as_view(),name='update_task'),
    path('tasklist/<int:pk>/delete',DeleteTask.as_view(),name='delete_task'),
]