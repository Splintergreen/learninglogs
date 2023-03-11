from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'learning_bot'


urlpatterns = [
    path('learning-bot', csrf_exempt(views.LearningBotView.as_view())),
]
