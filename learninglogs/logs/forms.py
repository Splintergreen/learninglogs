from django.forms import ModelForm

from .models import Log, Group
from django import forms


class LogForm(ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = Log
        fields = ('text', 'description', 'image',)
