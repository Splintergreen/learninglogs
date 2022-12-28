from django.contrib import admin

from .models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('date_added', 'owner', 'text', )


admin.site.register(Log)
