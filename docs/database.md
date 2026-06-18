# Banco de Dados

O banco alvo e PostgreSQL. Para desenvolvimento rapido e testes locais, `USE_SQLITE=true` troca para SQLite.

Entidades implementadas na Fase 1:

- `User`: perfil, papel, interesses, consentimentos LGPD e organizacao.
- `Organization`, `School`, `Classroom`, `OrganizationMember`.
- `Team`, `TeamMember`.
- `LearningPath`, `CourseCategory`, `Course`, `CourseInstructor`, `CourseModule`, `Lesson`.
- `Enrollment`, `LessonProgress`.

Todos os modelos de negocio principais usam identificador interno numerico e `public_id` UUID onde faz sentido para exposicao futura.
