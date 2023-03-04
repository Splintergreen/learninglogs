from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LogsViewSet


app_name = 'api'
router = DefaultRouter()

router.register('logs', LogsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# logs list
# add new log
# search
# last update
