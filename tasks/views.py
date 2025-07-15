
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from .forms import TaskForm
import json

def task_list(request):
    """
    Display the list of tasks and handle task creation (AJAX or regular POST).
    """
    tasks = Task.objects.all().order_by('-created_at')
    form = TaskForm()

    if request.method == 'POST':
        # Handle AJAX request
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
                form = TaskForm(data)
                if form.is_valid():
                    task = form.save()
                    return JsonResponse({
                        'status': 'ok',
                        'task': {
                            'id': task.id,
                            'title': task.title,
                            'description': task.description,
                            'completed': task.completed,
                        }
                    })
                else:
                    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        # Handle regular form POST
        else:
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('task_list')

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})

def complete_task(request, task_id):
    """
    Toggle the completion status of a task (regular POST only).
    """
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@csrf_exempt
def delete_task(request, task_id):
    """
    Delete a task. Accepts POST (AJAX) or GET (fallback).
    """
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return JsonResponse({'status': 'ok'})
    else:
        task.delete()
        return redirect('task_list')

@csrf_exempt
def toggle_task_completion(request, task_id):
    """
    Toggle the completion status of a task via AJAX POST.
    """
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()
            return JsonResponse({'status': 'ok', 'completed': task.completed})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return HttpResponseBadRequest('Only POST allowed')