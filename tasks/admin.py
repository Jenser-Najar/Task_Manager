from django.contrib import admin
from .models import Task

# Register the Task model in the Django admin interface
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "completed", "created_at")
    search_fields = ("title", "description")
    list_filter = ("completed", "created_at")