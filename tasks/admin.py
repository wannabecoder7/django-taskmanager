from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "deadline", "created_at", "updated_at")
    list_filter = ("status", "user", "deadline")
    search_fields = ("title", "user__username")
    ordering = ("-created_at",)
