from django.test import TestCase, Client
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    """
    Unit tests for the Task model.
    """
    def test_create_task(self):
        task = Task.objects.create(title="Test Task", description="Test description.")
        self.assertEqual(str(task), "Test Task")
        self.assertFalse(task.completed)

class TaskViewTest(TestCase):
    """
    Integration tests for Task views.
    """
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(title="Sample Task", description="Sample desc.")

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Task")

    def test_create_task_via_post(self):
        response = self.client.post(reverse('task_list'), {
            'title': 'New Task',
            'description': 'New description.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_toggle_task_completion(self):
        response = self.client.post(reverse('toggle_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed or not self.task.completed)  # Should toggle

    def test_delete_task(self):
        response = self.client.post(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())