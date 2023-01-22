from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Log, Group, Comment
from .models import User


admin.site.register(User)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    text = forms.CharField(widget=CKEditorWidget())
    list_display = ('text', 'description', 'owner', 'date_added', )
    search_fields = ('owner', 'text', )
    list_filter = ('owner', 'date_added', )
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    description = forms.CharField(widget=CKEditorWidget())
    logs = forms.ModelMultipleChoiceField(
        queryset=Log.objects.all(), required=True
    )
    list_display = ('title', 'description', 'owner', 'date_added',)
    search_fields = ('title', )
    list_filter = ('date_added', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    text = forms.CharField(widget=CKEditorWidget())
    list_display = ('text', 'author', 'created',)
    search_fields = ('author', 'text', )
    list_filter = ('author', 'created', )
    empty_value_display = '-пусто-'
