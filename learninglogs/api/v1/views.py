from logs.models import Log
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import LogSerializer


class LogsViewSet(ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
