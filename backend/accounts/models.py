from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Aluno"
        TEACHER = "teacher", "Professor"
        MENTOR = "mentor", "Mentor"
        SCHOOL_MANAGER = "school_manager", "Gestor de escola"
        ORG_MANAGER = "org_manager", "Gestor de organizacao"
        CONTENT_EDITOR = "content_editor", "Editor de conteudo"
        MODERATOR = "moderator", "Moderador"
        ADMIN = "admin", "Administrador"

    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=180)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.STUDENT, db_index=True)
    photo = models.ImageField(upload_to="users/photos/", blank=True, null=True)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=80, default="Brasil")
    interests = models.JSONField(default=list, blank=True)
    robotics_programs = models.JSONField(default=list, blank=True)
    organization = models.ForeignKey(
        "organizations.Organization",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )
    accepted_terms_at = models.DateTimeField(null=True, blank=True)
    privacy_consent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

    def __str__(self):
        return self.full_name or self.email

    @property
    def is_platform_admin(self):
        return self.is_superuser or self.role == self.Role.ADMIN
