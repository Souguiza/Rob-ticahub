from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from courses.models import Course, CourseCategory, CourseInstructor, CourseModule, LearningPath, Lesson
from organizations.models import Organization, OrganizationMember, Team, TeamMember

User = get_user_model()


DEMO_USERS = [
    ("admin@roboticahub.com", "Admin123!", "Administrador RoboticaHub", "admin", True, True),
    ("professor@roboticahub.com", "Professor123!", "Professora Ana Souza", "teacher", False, False),
    ("mentor@roboticahub.com", "Mentor123!", "Mentor Carlos Lima", "mentor", False, False),
    ("aluno@roboticahub.com", "Aluno123!", "Aluno Pedro Silva", "student", False, False),
]

DEMO_COURSES = {
    "Introducao a Robotica Competitiva": [
        "fundamentos",
        "sensores",
        "motores",
        "logica",
        "mecanica",
        "organizacao de equipe",
        "seguranca",
    ],
    "LEGO SPIKE Prime com Python": [
        "conhecendo o kit",
        "motores",
        "sensores",
        "giroscopio",
        "funcoes",
        "movimentacao",
        "programacao assincrona",
    ],
    "Seguidor de Linha e Controle PID": [
        "leitura de sensores",
        "calibracao",
        "erro",
        "controle proporcional",
        "integral",
        "derivativo",
        "PID",
        "recuperacao de linha",
    ],
    "Preparacao para FLL": [
        "estrategia",
        "missoes",
        "projeto do robo",
        "projeto de inovacao",
        "valores fundamentais",
        "apresentacao",
    ],
    "Introducao a OBR": [
        "pista",
        "seguidor de linha",
        "verde",
        "obstaculos",
        "rampa",
        "resgate",
        "preparacao para competicao",
    ],
}


class Command(BaseCommand):
    help = "Cria dados de demonstracao para desenvolvimento local."

    def handle(self, *args, **options):
        org, _ = Organization.objects.get_or_create(
            name="Instituto Robotica Brasil",
            defaults={
                "legal_name": "Instituto Robotica Brasil",
                "description": "Organizacao de demonstracao para o RoboticaHub Brasil.",
                "city": "Cuiaba",
                "state": "MT",
            },
        )

        users = {}
        for email, password, full_name, role, is_staff, is_superuser in DEMO_USERS:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "full_name": full_name,
                    "role": role,
                    "organization": org,
                    "city": "Cuiaba",
                    "state": "MT",
                    "accepted_terms_at": timezone.now(),
                    "privacy_consent_at": timezone.now(),
                    "is_staff": is_staff,
                    "is_superuser": is_superuser,
                },
            )
            if created:
                user.set_password(password)
                user.save()
            users[role] = user
            OrganizationMember.objects.get_or_create(organization=org, user=user, defaults={"role": role})

        team, _ = Team.objects.get_or_create(
            name="Tera Robotics",
            defaults={
                "team_number": "17730",
                "program": Team.Program.FTC,
                "description": "Equipe FTC de demonstracao.",
                "organization": org,
                "lead_mentor": users["mentor"],
                "season_year": 2026,
            },
        )
        TeamMember.objects.get_or_create(team=team, user=users["mentor"], defaults={"role": TeamMember.TeamRole.MENTOR})
        TeamMember.objects.get_or_create(team=team, user=users["student"], defaults={"role": TeamMember.TeamRole.PROGRAMMER})

        category, _ = CourseCategory.objects.get_or_create(name="Robotica Competitiva", slug="robotica-competitiva")
        path, _ = LearningPath.objects.get_or_create(
            title="Trilha Fundamentos de Robotica",
            defaults={"description": "Base para alunos e equipes iniciarem em robotica educacional."},
        )

        for index, (title, modules) in enumerate(DEMO_COURSES.items(), start=1):
            course, _ = Course.objects.get_or_create(
                slug=self.slugify(title),
                defaults={
                    "title": title,
                    "description": f"Curso de demonstracao: {title}.",
                    "category": category,
                    "level": Course.Level.BEGINNER if index < 3 else Course.Level.INTERMEDIATE,
                    "workload_hours": 8 + index,
                    "organization": org,
                    "status": "published",
                    "published_at": timezone.now(),
                    "requirements": "Curiosidade, trabalho em equipe e acesso a um computador.",
                    "objectives": "Desenvolver fundamentos praticos para competicoes e projetos.",
                    "created_by": users["teacher"],
                },
            )
            course.learning_paths.add(path)
            CourseInstructor.objects.get_or_create(course=course, user=users["teacher"])
            for order, module_title in enumerate(modules, start=1):
                module, _ = CourseModule.objects.get_or_create(
                    course=course,
                    order=order,
                    defaults={"title": module_title.title(), "created_by": users["teacher"]},
                )
                Lesson.objects.get_or_create(
                    module=module,
                    order=1,
                    defaults={
                        "title": f"Aula inicial: {module_title.title()}",
                        "lesson_type": Lesson.LessonType.TEXT,
                        "content": "Conteudo introdutorio de demonstracao para validar o fluxo do LMS.",
                        "duration_minutes": 12,
                        "created_by": users["teacher"],
                    },
                )

        self.stdout.write(self.style.SUCCESS("Dados de demonstracao criados/atualizados."))

    def slugify(self, value):
        return (
            value.lower()
            .replace(" ", "-")
            .replace("ç", "c")
            .replace("ã", "a")
            .replace("á", "a")
            .replace("ó", "o")
            .replace("í", "i")
        )
