"""
Main URL configuration for the Task Manager project.

Routes:
    /admin/  - Django admin interface
    /        - Task Manager app (all task-related URLs)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('', include('tasks.urls')),  # Task Manager app
]
