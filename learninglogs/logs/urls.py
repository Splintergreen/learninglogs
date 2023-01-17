from django.urls import path
from . import views

app_name = 'logs'


urlpatterns = [
    path('', views.index, name='index'),
    path('groups/', views.groups, name='groups_list'),
    path('create/', views.create_log, name='create_log'),
    path(
        'log/<int:pk>/edit/',
        views.edit_log,
        name='edit_log'
    ),
    # path('logs/', views.logs, name='log_list'),
    path('group/<int:pk>/', views.group, name='group'),
    path('log/<int:pk>/', views.log, name='log'),
    path('search/', views.search, name='search'),
    path('my-logs/', views.my_logs, name='my_logs'),
    path('profile/', views.profile_settings, name='profile_settings'),
    # path('contacts/', views.contacts, name='contacts')
]
