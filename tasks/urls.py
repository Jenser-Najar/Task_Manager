from django.urls import path
from .views import task_list, complete_task, delete_task, toggle_task_completion

urlpatterns = [
    path('', task_list, name='task_list'),
    path('complete/<int:task_id>/', complete_task, name='complete_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', toggle_task_completion, name='toggle_task'),
]