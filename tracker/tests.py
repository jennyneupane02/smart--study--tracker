from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Task


class TrackerTests(TestCase):
    # These tests check that authentication and the task API work correctly.
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='testpass123')
        self.task = Task.objects.create(
            user=self.user,
            title='Read chapter 1',
            description='Prepare notes for class',
            deadline=timezone.now() + timezone.timedelta(days=1),
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_toggle_task_api(self):
        self.client.login(username='student', password='testpass123')
        response = self.client.post(reverse('toggle_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
