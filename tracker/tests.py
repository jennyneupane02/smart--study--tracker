import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import DailyGoal, StudySession, Subject, Task


class TaskModelTests(TestCase):
    # These tests check important Task model behavior so model bugs are caught early.
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='testpass123')

    def test_task_string_returns_title(self):
        # __str__ should return the task title so tasks display clearly in the admin and shell.
        task = Task.objects.create(
            user=self.user,
            title='Read chapter 1',
            description='Prepare notes for class',
            deadline=timezone.now() + timezone.timedelta(days=1),
        )
        self.assertEqual(str(task), 'Read chapter 1')

    def test_task_is_overdue_property(self):
        # is_overdue should be True only when an incomplete task deadline is in the past.
        task = Task.objects.create(
            user=self.user,
            title='Past homework',
            deadline=timezone.now() - timezone.timedelta(days=1),
        )
        self.assertTrue(task.is_overdue)

    def test_completed_task_is_not_overdue(self):
        # A completed task should not be marked overdue, even if its deadline has passed.
        task = Task.objects.create(
            user=self.user,
            title='Finished homework',
            deadline=timezone.now() - timezone.timedelta(days=1),
            completed=True,
        )
        self.assertFalse(task.is_overdue)


class DashboardViewTests(TestCase):
    # These tests check that dashboard access and dashboard data work for logged-in users.
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='testpass123')
        self.subject = Subject.objects.create(user=self.user, name='Computer Science')
        Task.objects.create(
            user=self.user,
            subject=self.subject,
            title='Practice Django',
            deadline=timezone.now() + timezone.timedelta(days=1),
        )
        DailyGoal.objects.create(
            user=self.user,
            date=timezone.localdate(),
            target_minutes=60,
            target_tasks=2,
        )
        StudySession.objects.create(
            user=self.user,
            subject=self.subject,
            date=timezone.localdate(),
            minutes=30,
        )

    def test_dashboard_requires_login(self):
        # A visitor who is not logged in should be redirected instead of seeing private data.
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated_user_gets_200(self):
        # A logged-in user should be able to open the dashboard successfully.
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_context_contains_progress_data(self):
        # The dashboard should calculate study minutes and task totals for the current user.
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context['studied_minutes'], 30)
        self.assertEqual(response.context['total_count'], 1)


class TaskAPITests(TestCase):
    # These tests check the JSON endpoint used by JavaScript on the tasks page.
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='testpass123')
        self.other_user = User.objects.create_user(username='other', password='testpass123')
        self.task = Task.objects.create(
            user=self.user,
            title='Read chapter 1',
            description='Prepare notes for class',
            deadline=timezone.now() + timezone.timedelta(days=1),
        )

    def test_toggle_task_api_changes_task_status(self):
        # A logged-in user should be able to toggle their own task from incomplete to complete.
        self.client.login(username='student', password='testpass123')
        response = self.client.post(reverse('toggle_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_toggle_task_api_returns_correct_json_shape(self):
        # The JavaScript depends on these JSON keys to update the page without a reload.
        self.client.login(username='student', password='testpass123')
        response = self.client.post(reverse('toggle_task', args=[self.task.id]))
        data = json.loads(response.content)
        self.assertEqual(data['success'], True)
        self.assertIn('task_id', data)
        self.assertIn('completed', data)
        self.assertIn('completed_count', data)
        self.assertIn('total_count', data)
        self.assertIn('percent', data)

    def test_toggle_task_requires_login(self):
        # An unauthenticated user should be redirected instead of receiving private JSON data.
        response = self.client.post(reverse('toggle_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_toggle_another_users_task(self):
        # A logged-in user should not be allowed to change a task owned by someone else.
        self.client.login(username='other', password='testpass123')
        response = self.client.post(reverse('toggle_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 404)
