from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating Task instances.
    Uses custom widgets for better UI/UX.
    """
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
                'rows': 3,
                'class': 'task-input',
                'autocomplete': 'off',
            }),
        }