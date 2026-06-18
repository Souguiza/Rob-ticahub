import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from courses.models import Course, CourseCategory

User = get_user_model()


@pytest.mark.django_db
def test_user_can_register_and_login():
    client = APIClient()
    payload = {
        "email": "novo@roboticahub.com",
        "password": "SenhaForte123!",
        "full_name": "Novo Aluno",
        "city": "Cuiaba",
        "state": "MT",
        "country": "Brasil",
        "interests": ["FLL"],
        "robotics_programs": ["FLL"],
        "accepted_terms": True,
        "privacy_consent": True,
    }

    response = client.post("/api/auth/register/", payload, format="json")
    assert response.status_code == 201

    login = client.post("/api/auth/login/", {"email": payload["email"], "password": payload["password"]}, format="json")
    assert login.status_code == 200
    assert "access" in login.data


@pytest.mark.django_db
def test_student_cannot_create_course():
    client = APIClient()
    user = User.objects.create_user(
        email="aluno@test.com",
        password="Aluno123!",
        full_name="Aluno Teste",
        accepted_terms_at=timezone.now(),
        privacy_consent_at=timezone.now(),
    )
    client.force_authenticate(user=user)
    category = CourseCategory.objects.create(name="Robotica", slug="robotica")

    response = client.post(
        "/api/courses/",
        {
            "title": "Curso Restrito",
            "slug": "curso-restrito",
            "description": "Nao deve ser criado por aluno.",
            "category": category.id,
            "level": Course.Level.BEGINNER,
            "workload_hours": 4,
            "status": "published",
        },
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_teacher_can_create_course():
    client = APIClient()
    teacher = User.objects.create_user(
        email="prof@test.com",
        password="Professor123!",
        full_name="Professor Teste",
        role=User.Role.TEACHER,
        accepted_terms_at=timezone.now(),
        privacy_consent_at=timezone.now(),
    )
    category = CourseCategory.objects.create(name="Programacao", slug="programacao")
    client.force_authenticate(user=teacher)

    response = client.post(
        "/api/courses/",
        {
            "title": "Python para Robos",
            "slug": "python-para-robos",
            "description": "Base de programacao para robotica.",
            "category": category.id,
            "level": Course.Level.BEGINNER,
            "workload_hours": 6,
            "status": "published",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["created_by"] == teacher.id
