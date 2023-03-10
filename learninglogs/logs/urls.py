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
    path(
        'log/<int:pk>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'comment/<int:pk>/delete/',
        views.delete_comment,
        name='delete_comment'
    ),
    path('group/<int:pk>/', views.group, name='group'),
    path('log/<int:pk>/', views.log, name='log'),
    path('search/', views.search, name='search'),
    path('my-logs/', views.my_logs, name='my_logs'),
    path('user/<str:username>/logs/', views.user_logs, name='user_logs'),
    path('profile/', views.profile_settings, name='profile_settings'),
    path('like/', views.like, name="like"),
    path('favorite/', views.favorite_logs, name="favorite"),
]
