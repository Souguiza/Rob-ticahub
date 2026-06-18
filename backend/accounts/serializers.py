from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "photo",
            "biography",
            "birth_date",
            "city",
            "state",
            "country",
            "interests",
            "robotics_programs",
            "organization",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "role", "is_active", "created_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    accepted_terms = serializers.BooleanField(write_only=True)
    privacy_consent = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "full_name",
            "city",
            "state",
            "country",
            "interests",
            "robotics_programs",
            "accepted_terms",
            "privacy_consent",
        ]

    def validate(self, attrs):
        if not attrs.get("accepted_terms") or not attrs.get("privacy_consent"):
            raise serializers.ValidationError("Termos e politica de privacidade precisam ser aceitos.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("accepted_terms")
        validated_data.pop("privacy_consent")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.accepted_terms_at = timezone.now()
        user.privacy_consent_at = timezone.now()
        user.set_password(password)
        user.save()
        return user
