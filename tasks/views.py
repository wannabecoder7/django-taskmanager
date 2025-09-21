from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # admins and superusers see all tasks
        if user.is_staff or user.is_superuser:
            return Task.objects.all().order_by("-created_at")
        # normal users see only their tasks
        return Task.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        """
        - If requester is admin/superuser:
            * if the client provided a user (serializer.validated_data contains 'user'), honor it
            * otherwise default to request.user (so DB user FK is never NULL)
        - If requester is a normal user: always force user=request.user
        """
        request_user = self.request.user

        # serializer.validated_data is available here (create() / perform_create runs after validation)
        assigned_user = serializer.validated_data.get("user") if hasattr(serializer, "validated_data") else None

        if request_user.is_staff or request_user.is_superuser:
            if assigned_user:
                serializer.save()          # admin explicitly assigned user -> honor it
            else:
                serializer.save(user=request_user)  # admin didn't assign -> default to admin (or you could default to None if allowed)
        else:
            # normal users cannot assign tasks to others
            serializer.save(user=request_user)

    def perform_update(self, serializer):
        """
        - Admins can update & reassign (if they include user in payload)
        - Normal users cannot change owner: force user=request.user
        """
        request_user = self.request.user

        if request_user.is_staff or request_user.is_superuser:
            serializer.save()
        else:
            serializer.save(user=request_user)
