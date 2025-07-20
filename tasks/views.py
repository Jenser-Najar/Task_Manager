
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from .forms import TaskForm

def task_list(request):
    """
    Display the list of tasks and handle task creation
    """
    tasks = Task.objects.all().order_by('-created_at')
    form = TaskForm()


    if request.method == 'POST':
        # AJAX: fetch() sends as multipart/form-data, not JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save()
                from django.template.loader import render_to_string
                task_html = render_to_string('tasks/_task_item.html', {'task': task})
                return JsonResponse({'status': 'ok', 'task_html': task_html})
            else:
                errors = '\n'.join([f"{k}: {v[0]}" for k, v in form.errors.items()])
                return JsonResponse({'status': 'error', 'errors': errors}, status=400)
        else:
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('task_list')

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})

def complete_task(task_id):
    """
    Mark a task as completed or not completed
    """
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@csrf_exempt
def delete_task(request, task_id):
    """
    Delete a task
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
    This function allows changing the completion status of a task
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