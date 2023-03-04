from django.contrib.auth import get_user_model
from logs.models import Log
from rest_framework import serializers

User = get_user_model()


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
