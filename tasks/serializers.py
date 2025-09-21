# tasks/serializers.py
from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model
from notes.serializers import NoteSerializer  # assuming you already have this

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class TaskSerializer(serializers.ModelSerializer):
    # Read-only nested representation of the user
    user = UserSerializer(read_only=True)

    # Write-only field for assigning user by id (admins only)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",  # maps to Task.user
        write_only=True,
        required=False,
    )

    # Keep notes as read-only
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "created_at",
            "updated_at",
            "user",      # nested, read-only
            "user_id",   # write-only
            "notes",
        ]
