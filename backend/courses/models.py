from django.conf import settings
from django.db import models

from common.models import TimestampedModel


class CourseCategory(TimestampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class LearningPath(TimestampedModel):
    title = models.CharField(max_length=180, db_index=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=24, default="published", db_index=True)

    def __str__(self):
        return self.title


class Course(TimestampedModel):
    class Level(models.TextChoices):
        BEGINNER = "beginner", "Iniciante"
        INTERMEDIATE = "intermediate", "Intermediario"
        ADVANCED = "advanced", "Avancado"

    class Modality(models.TextChoices):
        ONLINE = "online", "Online"
        HYBRID = "hybrid", "Hibrido"
        PRESENTIAL = "presential", "Presencial"

    title = models.CharField(max_length=220, db_index=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="courses/covers/", blank=True, null=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True, related_name="courses")
    learning_paths = models.ManyToManyField(LearningPath, blank=True, related_name="courses")
    level = models.CharField(max_length=24, choices=Level.choices, default=Level.BEGINNER)
    workload_hours = models.PositiveIntegerField(default=1)
    organization = models.ForeignKey("organizations.Organization", on_delete=models.SET_NULL, null=True, blank=True)
    modality = models.CharField(max_length=24, choices=Modality.choices, default=Modality.ONLINE)
    is_free = models.BooleanField(default=True)
    status = models.CharField(max_length=24, default="draft", db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    requirements = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    certificate_available = models.BooleanField(default=True)
    minimum_completion_percent = models.PositiveIntegerField(default=80)

    def __str__(self):
        return self.title


class CourseInstructor(TimestampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="instructors")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="instructed_courses")
    role = models.CharField(max_length=80, default="Instrutor")

    class Meta:
        unique_together = ("course", "user")


class CourseModule(TimestampedModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=24, default="published", db_index=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Lesson(TimestampedModel):
    class LessonType(models.TextChoices):
        TEXT = "text", "Texto"
        VIDEO = "video", "Video"
        PDF = "pdf", "PDF"
        FILE = "file", "Arquivo"
        CODE = "code", "Codigo"
        ASSIGNMENT = "assignment", "Atividade"
        QUIZ = "quiz", "Quiz"
        EXTERNAL_LINK = "external_link", "Link externo"

    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=180)
    lesson_type = models.CharField(max_length=32, choices=LessonType.choices, default=LessonType.TEXT)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    file = models.FileField(upload_to="courses/lessons/", blank=True, null=True)
    external_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=24, default="published", db_index=True)

    class Meta:
        ordering = ["module", "order", "title"]

    def __str__(self):
        return self.title


class Enrollment(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=24, default="active", db_index=True)
    progress_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "course")


class LessonProgress(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="lesson_progress")
    is_completed = models.BooleanField(default=False, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_position_seconds = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "lesson")
