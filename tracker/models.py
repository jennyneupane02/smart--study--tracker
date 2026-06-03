from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Subject(models.Model):
    # A subject groups a user's study tasks, such as Math, English, or Computer Science.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=80)
    color = models.CharField(max_length=20, default='blue')

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    # A task represents one study responsibility or assignment that belongs to a user.
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['completed', 'deadline']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return not self.completed and self.deadline < timezone.now()


class StudySession(models.Model):
    # A study session stores how much time the user studied for a selected subject on a date.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='study_sessions')
    date = models.DateField(default=timezone.now)
    minutes = models.PositiveIntegerField(default=30)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} - {self.minutes} minutes'


class DailyGoal(models.Model):
    # A daily goal stores a simple study target for the user.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_goals')
    date = models.DateField(default=timezone.now)
    target_minutes = models.PositiveIntegerField(default=60)
    target_tasks = models.PositiveIntegerField(default=2)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} goal for {self.date}'
