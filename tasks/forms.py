from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Task title',
                'class': 'task-input',
                'maxlength': 255,
                'autocomplete': 'off',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Description (optional)',
                'rows': 5,
                'class': 'task-input',
                'autocomplete': 'off',
            }),
        }