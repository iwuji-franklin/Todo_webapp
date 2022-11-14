from ast import pattern
from django.contrib import admin
admin.autodiscover()
from django.urls import path, re_path
from . import views

app_name = 'todo_app'

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^task-detail/(?P<slug>[-\w]+)/$',views.show_task, name='task_detail'),
    path('change-status/(?P<slug>[-\w]+)/', views.change_status, name='change_status'),
]
