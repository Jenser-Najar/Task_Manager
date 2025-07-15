
from django.urls import path
from .views import task_list, complete_task, delete_task, toggle_task_completion

# URL patterns for the Task Manager app
# Each path is mapped to a view function in views.py
urlpatterns = [
    path('', task_list, name='task_list'),  # Main page: list and add tasks
    path('complete/<int:task_id>/', complete_task, name='complete_task'),  # Toggle completion (regular POST)
    path('delete/<int:task_id>/', delete_task, name='delete_task'),        # Delete a task (AJAX or GET)
    path('toggle/<int:task_id>/', toggle_task_completion, name='toggle_task'),  # Toggle completion (AJAX)
]