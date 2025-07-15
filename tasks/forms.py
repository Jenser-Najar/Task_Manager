from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título de la tarea'}),
            'description': forms.Textarea(attrs={'placeholder': 'Descripción (opcional)', 'rows': 3}),
        }