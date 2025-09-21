from django.db import models
from django.conf import settings

class Task(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[("TODO", "To Do"), ("IN_PROGRESS", "In Progress"), ("DONE", "Done")],
        default="TODO",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    deadline = models.DateField(null=True, blank=True)  # <-- NEW

    def __str__(self):
        return f"{self.title} ({self.status})"
