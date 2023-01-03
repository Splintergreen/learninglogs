# from django.contrib import admin
from django.urls import path
from . import views

app_name = 'logs'


urlpatterns = [
    path('', views.index, name='index'),
    path('groups/', views.groups, name='groups_list'),
    # path('logs/', views.logs, name='log_list'),
    path('group/<int:pk>/', views.group, name='group'),
    path('log/<int:pk>/', views.log, name='log'),
    # path('contacts/', views.contacts, name='contacts')
]
