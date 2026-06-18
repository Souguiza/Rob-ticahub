from rest_framework import permissions, viewsets

from accounts.permissions import CanManageCourses
from courses.models import Course, Enrollment, LearningPath, LessonProgress
from courses.serializers import CourseSerializer, EnrollmentSerializer, LearningPathSerializer, LessonProgressSerializer


class LearningPathViewSet(viewsets.ModelViewSet):
    serializer_class = LearningPathSerializer
    queryset = LearningPath.objects.filter(is_deleted=False).order_by("title")
    permission_classes = [CanManageCourses]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.prefetch_related("modules__lessons", "learning_paths").filter(is_deleted=False).order_by("title")
    permission_classes = [CanManageCourses]
    search_fields = ["title", "description", "objectives"]
    filterset_fields = ["level", "status", "is_free", "category"]
    ordering_fields = ["title", "published_at", "workload_hours"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role in {"teacher", "content_editor", "admin"}:
            return qs
        return qs.filter(status="published")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "course"]

    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            return Enrollment.objects.select_related("user", "course").all()
        return Enrollment.objects.select_related("course").filter(user=user)


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            return LessonProgress.objects.select_related("user", "lesson", "enrollment").all()
        return LessonProgress.objects.select_related("lesson", "enrollment").filter(user=user)
