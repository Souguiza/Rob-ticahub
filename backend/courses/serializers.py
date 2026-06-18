from django.utils import timezone
from rest_framework import serializers

from courses.models import Course, CourseModule, Enrollment, LearningPath, Lesson, LessonProgress


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = CourseModule
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    modules = CourseModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at", "public_id"]


class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPath
        fields = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"
        read_only_fields = ["user", "progress_percent", "started_at", "completed_at", "created_by"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = "__all__"
        read_only_fields = ["user", "created_by", "completed_at"]

    def validate(self, attrs):
        request = self.context["request"]
        enrollment = attrs["enrollment"]
        if enrollment.user_id != request.user.id:
            raise serializers.ValidationError("A matricula informada nao pertence ao usuario autenticado.")
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user
        validated_data["created_by"] = request.user
        if validated_data.get("is_completed"):
            validated_data["completed_at"] = timezone.now()
        progress = super().create(validated_data)
        self._recalculate(progress.enrollment)
        return progress

    def update(self, instance, validated_data):
        if validated_data.get("is_completed") and not instance.completed_at:
            validated_data["completed_at"] = timezone.now()
        progress = super().update(instance, validated_data)
        self._recalculate(progress.enrollment)
        return progress

    def _recalculate(self, enrollment):
        total = Lesson.objects.filter(module__course=enrollment.course, status="published").count()
        done = LessonProgress.objects.filter(enrollment=enrollment, is_completed=True).count()
        enrollment.progress_percent = round((done / total) * 100, 2) if total else 0
        if enrollment.progress_percent >= enrollment.course.minimum_completion_percent and not enrollment.completed_at:
            enrollment.completed_at = timezone.now()
            enrollment.status = "completed"
        enrollment.save(update_fields=["progress_percent", "completed_at", "status", "updated_at"])
