from django.forms import ModelForm

from .models import Log, Group, User, Comment
from django import forms
from ckeditor.widgets import CKEditorWidget

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
    # text = forms.CharField(label="", widget=CKEditorWidget(attrs={'class': 'form-control'}))
    # text = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here!!!', }))
    class Meta:
        model = Comment
        fields = ('text', )
