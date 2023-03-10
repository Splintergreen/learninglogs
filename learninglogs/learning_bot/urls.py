from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name = 'learning_bot'


urlpatterns = [
    path('learning-bot', csrf_exempt(views.LearningBotView.as_view())),
]
