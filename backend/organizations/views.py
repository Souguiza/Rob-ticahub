from rest_framework import permissions, viewsets

from organizations.models import Organization, Team
from organizations.serializers import OrganizationSerializer, TeamSerializer


class AdminWritePermission(permissions.BasePermission):
    manager_roles = {"org_manager", "school_manager", "mentor", "admin"}

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_platform_admin or request.user.role in self.manager_roles
        )


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.filter(is_deleted=False).order_by("name")
    permission_classes = [AdminWritePermission]
    search_fields = ["name", "city", "state"]
    ordering_fields = ["name", "created_at"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.select_related("organization", "lead_mentor").filter(is_deleted=False).order_by("name")
    permission_classes = [AdminWritePermission]
    search_fields = ["name", "team_number", "program"]
    filterset_fields = ["program", "organization", "season_year", "status"]
    ordering_fields = ["name", "season_year", "created_at"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
