from django.contrib import admin

from .models import Event, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'admin_image']
    prepopulated_fields = {'slug': ('name',)}


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'get_staff_count', 'get_participant_count', 'category', 'admin_image']
    list_filter = ['available', 'created', 'updated']
    search_fields = ['name', ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
