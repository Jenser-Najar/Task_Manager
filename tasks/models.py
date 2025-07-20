from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=125, help_text="Title of the task.")
    description = models.TextField(max_length=425, blank=True, help_text="Optional description of the task.")
    completed = models.BooleanField(default=False, help_text="Whether the task is completed.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the task was created.")

    def __str__(self):
        """String representation: returns the task title."""
        return str(self.title)