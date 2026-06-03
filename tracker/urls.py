from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('subjects/', views.subjects, name='subjects'),
    path('sessions/', views.sessions, name='sessions'),
    path('goals/', views.goals, name='goals'),
    path('api/tasks/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
]
