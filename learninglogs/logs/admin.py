from django.contrib import admin

from .models import Log, Group


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('text', 'description', 'owner', 'date_added', )
    search_fields = ('owner', 'text', )
    list_filter = ('owner', 'date_added', )
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'date_added',)
    search_fields = ('title', )
    list_filter = ('date_added', )
