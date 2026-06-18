from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_platform_admin or obj == request.user


class RolePermission(BasePermission):
    allowed_roles = set()

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_platform_admin or request.user.role in self.allowed_roles)
        )


class CanManageCourses(BasePermission):
    allowed_roles = {"teacher", "content_editor", "org_manager", "admin"}

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role in self.allowed_roles)
