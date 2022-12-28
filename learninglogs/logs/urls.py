# from django.contrib import admin
from django.urls import path
from . import views

app_name = 'logs'


urlpatterns = [
    path('', views.index, name='index'),
    path('logs/', views.logs, name='log_list'),
    path('log/<int:pk>/', views.log, name='log'),
]
