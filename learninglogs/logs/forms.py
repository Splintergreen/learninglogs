from django.forms import ModelForm

from .models import Log, Group, User, Comment
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
            'about',
            'skills',
        )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
