from rest_framework import serializers

from organizations.models import Organization, Team, TeamMember


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at", "public_id"]


class TeamMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = TeamMember
        fields = ["id", "public_id", "team", "user", "user_name", "role", "status", "created_at"]
        read_only_fields = ["public_id", "created_at"]


class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(source="memberships", many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at", "public_id"]
