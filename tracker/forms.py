from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DailyGoal, StudySession, Subject, Task


class RegisterForm(UserCreationForm):
    # This form creates a new user account using Django's authentication system.
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SubjectForm(forms.ModelForm):
    # This form lets users create subjects for organizing their tasks.
    class Meta:
        model = Subject
        fields = ['name', 'color']


class TaskForm(forms.ModelForm):
    # This form lets users create or edit study tasks.
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ['subject', 'title', 'description', 'deadline', 'priority']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)


class StudySessionForm(forms.ModelForm):
    # This form records study time for a date and subject.
    class Meta:
        model = StudySession
        fields = ['subject', 'date', 'minutes', 'notes']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)


class DailyGoalForm(forms.ModelForm):
    # This form lets users set a daily goal for study minutes and completed tasks.
    class Meta:
        model = DailyGoal
        fields = ['date', 'target_minutes', 'target_tasks']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}
