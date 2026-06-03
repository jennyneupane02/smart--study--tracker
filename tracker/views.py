from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import DailyGoalForm, RegisterForm, StudySessionForm, SubjectForm, TaskForm
from .models import DailyGoal, StudySession, Subject, Task


def index(request):
    # This view displays the public home page and changes content based on login status.
    return render(request, 'tracker/index.html')


def register_view(request):
    # This view handles GET and POST requests for creating a new user account.
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account was created successfully.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})


@login_required
def dashboard(request):
    # This view shows the user's study summary, task counts, sessions, and daily goal progress.
    tasks = Task.objects.filter(user=request.user)
    completed_count = tasks.filter(completed=True).count()
    total_count = tasks.count()
    pending_tasks = tasks.filter(completed=False)[:5]
    today = timezone.localdate()
    today_sessions = StudySession.objects.filter(user=request.user, date=today)
    studied_minutes = sum(session.minutes for session in today_sessions)
    goal = DailyGoal.objects.filter(user=request.user, date=today).first()
    task_percent = int((completed_count / total_count) * 100) if total_count else 0
    minute_percent = int((studied_minutes / goal.target_minutes) * 100) if goal else 0
    return render(request, 'tracker/dashboard.html', {
        'tasks': tasks,
        'pending_tasks': pending_tasks,
        'completed_count': completed_count,
        'total_count': total_count,
        'task_percent': task_percent,
        'studied_minutes': studied_minutes,
        'goal': goal,
        'minute_percent': min(minute_percent, 100),
    })


@login_required
def tasks(request):
    # This view handles both GET and POST for listing and creating tasks.
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully.')
            return redirect('tasks')
    else:
        form = TaskForm(user=request.user)
    task_list = Task.objects.filter(user=request.user)
    return render(request, 'tracker/tasks.html', {'form': form, 'tasks': task_list})


@login_required
def edit_task(request, task_id):
    # This view lets a logged-in user edit only their own task.
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('tasks')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tracker/edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    # This view deletes a task after a POST confirmation.
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('tasks')
    return render(request, 'tracker/delete_task.html', {'task': task})


@login_required
def subjects(request):
    # This view handles GET and POST for subject creation and listing.
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, 'Subject added successfully.')
            return redirect('subjects')
    else:
        form = SubjectForm()
    return render(request, 'tracker/subjects.html', {'form': form, 'subjects': Subject.objects.filter(user=request.user)})


@login_required
def sessions(request):
    # This view handles GET and POST for recording study sessions.
    if request.method == 'POST':
        form = StudySessionForm(request.POST, user=request.user)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            messages.success(request, 'Study session saved successfully.')
            return redirect('sessions')
    else:
        form = StudySessionForm(user=request.user)
    session_list = StudySession.objects.filter(user=request.user)[:20]
    return render(request, 'tracker/sessions.html', {'form': form, 'sessions': session_list})


@login_required
def goals(request):
    # This view handles GET and POST for setting daily study goals.
    if request.method == 'POST':
        form = DailyGoalForm(request.POST)
        if form.is_valid():
            goal, created = DailyGoal.objects.update_or_create(
                user=request.user,
                date=form.cleaned_data['date'],
                defaults={
                    'target_minutes': form.cleaned_data['target_minutes'],
                    'target_tasks': form.cleaned_data['target_tasks'],
                }
            )
            messages.success(request, 'Goal saved successfully.')
            return redirect('goals')
    else:
        form = DailyGoalForm()
    goal_list = DailyGoal.objects.filter(user=request.user)[:14]
    return render(request, 'tracker/goals.html', {'form': form, 'goals': goal_list})


@login_required
@require_POST
def toggle_task(request, task_id):
    # This API view toggles a task's completed status and returns JSON for JavaScript.
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.completed_at = timezone.now() if task.completed else None
    task.save()
    total = Task.objects.filter(user=request.user).count()
    completed = Task.objects.filter(user=request.user, completed=True).count()
    percent = int((completed / total) * 100) if total else 0
    return JsonResponse({
        'success': True,
        'task_id': task.id,
        'completed': task.completed,
        'completed_count': completed,
        'total_count': total,
        'percent': percent,
    })
