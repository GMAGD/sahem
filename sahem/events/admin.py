from django.contrib import admin

from .models import Event, Category, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'admin_image']
    prepopulated_fields = {'slug': ('name',)}


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'get_staff_count', 'get_participant_count', 'category', 'admin_image']
    list_filter = ['available', 'created', 'updated']
    search_fields = ['name', ]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
