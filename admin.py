from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'created_date')
    list_filter = ('completed', 'created_date')
    search_fields = ('title', 'description', 'user__username')
