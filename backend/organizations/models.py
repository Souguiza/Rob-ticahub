from django.conf import settings
from django.db import models

from common.models import TimestampedModel


class Organization(TimestampedModel):
    name = models.CharField(max_length=180, db_index=True)
    legal_name = models.CharField(max_length=220, blank=True)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=80, default="Brasil")
    status = models.CharField(max_length=24, default="active", db_index=True)

    def __str__(self):
        return self.name


class School(TimestampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="schools")
    name = models.CharField(max_length=180)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=24, default="active", db_index=True)

    def __str__(self):
        return self.name


class Classroom(TimestampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="classrooms")
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name="classrooms")
    name = models.CharField(max_length=120)
    year = models.PositiveIntegerField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=24, default="active", db_index=True)

    def __str__(self):
        return f"{self.name} - {self.year}"


class OrganizationMember(TimestampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization_memberships")
    role = models.CharField(max_length=64)
    status = models.CharField(max_length=24, default="active", db_index=True)

    class Meta:
        unique_together = ("organization", "user")


class Team(TimestampedModel):
    class Program(models.TextChoices):
        FLL = "FLL", "FLL"
        FTC = "FTC", "FTC"
        FRC = "FRC", "FRC"
        OBR = "OBR", "OBR"
        ARDUINO = "ARDUINO", "Arduino"
        SPIKE = "SPIKE", "LEGO SPIKE Prime"
        FREE = "FREE", "Robotica livre"
        OTHER = "OTHER", "Outros"

    name = models.CharField(max_length=180, db_index=True)
    team_number = models.CharField(max_length=32, blank=True, db_index=True)
    program = models.CharField(max_length=24, choices=Program.choices)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="teams/logos/", blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="teams")
    lead_mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mentored_teams",
    )
    season_year = models.PositiveIntegerField()
    status = models.CharField(max_length=24, default="active", db_index=True)

    def __str__(self):
        return self.name


class TeamMember(TimestampedModel):
    class TeamRole(models.TextChoices):
        CAPTAIN = "captain", "Capitao"
        PROGRAMMER = "programmer", "Programador"
        DESIGNER = "designer", "Projetista"
        MECHANIC = "mechanic", "Mecanico"
        ELECTRICIAN = "electrician", "Eletricista"
        RESEARCHER = "researcher", "Pesquisador"
        DOCUMENTATION = "documentation", "Documentacao"
        PRESENTATION = "presentation", "Apresentacao"
        MENTOR = "mentor", "Mentor"
        MEMBER = "member", "Membro"

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_memberships")
    role = models.CharField(max_length=32, choices=TeamRole.choices, default=TeamRole.MEMBER)
    status = models.CharField(max_length=24, default="active", db_index=True)

    class Meta:
        unique_together = ("team", "user")
