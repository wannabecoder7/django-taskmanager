from rest_framework import serializers # Tools to convert Django models to JSON and back.
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password # Uses Django’s built-in password validators

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
          model = User
          fields = ["id", "username", "email", "is_staff"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data.get("email", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
