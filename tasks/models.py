from django.db import models

class Task(models.Model):
    """
    Represents a single to-do task in the Task Manager app.
    """
    title = models.CharField(max_length=255, help_text="Title of the task.")
    description = models.TextField(blank=True, help_text="Optional description of the task.")
    completed = models.BooleanField(default=False, help_text="Whether the task is completed.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the task was created.")

    def __str__(self):
        """String representation: returns the task title."""
        return self.title