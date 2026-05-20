from django.contrib import admin
from .models import DailyGoal, StudySession, Subject, Task

# Register all project models so they can be managed in Django Admin.
admin.site.register(Subject)
admin.site.register(Task)
admin.site.register(StudySession)
admin.site.register(DailyGoal)
