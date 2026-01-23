from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone", "location", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]
        read_only_fields = ["id"]


# FLAW 4: A07 - Authentication Failures
# No password strength requirements, users can create accounts with weak passwords such as "1", "a", "password"
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


# FIX: Add password strength validation
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError as DjangoValidationError
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True)
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ["username", "email", "password", "password2"]
#
#     def validate(self, attrs):
#         if attrs["password"] != attrs["password2"]:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#
#         # SAFE: Validate password strength using Django's built-in validators
#         try:
#             validate_password(attrs["password"])
#         except DjangoValidationError as e:
#             raise serializers.ValidationError({"password": list(e.messages)})
#
#         return attrs
#
#     def create(self, validated_data):
#         validated_data.pop("password2")
#         user = User.objects.create_user(**validated_data)
#         UserProfile.objects.create(user=user)
#         return user
#
# Also add to settings.py:
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]
