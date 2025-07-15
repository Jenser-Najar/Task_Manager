from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    form = TaskForm(request.POST or None)

    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            # AJAX
            import json
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
        else:
            # Formulario tradicional
            if form.is_valid():
                form.save()
                return redirect('task_list')

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@csrf_exempt  # Solo si no usas token CSRF en JS
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return JsonResponse({'status': 'ok'})
    else:
        # Para compatibilidad con el enlace normal
        task.delete()
        return redirect('task_list')

@csrf_exempt  # Solo si no estás usando el token CSRF en JS, lo quitamos luego si lo agregamos.
def toggle_task_completion(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()
            return JsonResponse({'status': 'ok', 'completed': task.completed})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return HttpResponseBadRequest('Only POST allowed')