from django.contrib import admin

from .models import Event


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'get_staff_count', 'get_participant_count', ]


admin.site.register(Event, EventAdmin)
