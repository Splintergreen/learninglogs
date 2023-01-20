from django.forms import ModelForm

from .models import Log, Group, User
from django import forms


class LogForm(ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = Log
        fields = ('text', 'description', 'image',)


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'avatar',
            'first_name',
            'last_name',
            'email',
            'about',
            'skills',
        )
