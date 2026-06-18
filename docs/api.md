# API

Documentacao interativa: `/api/docs/`

Endpoints da Fase 1:

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`
- `GET /api/courses/`
- `POST /api/courses/`
- `GET /api/learning-paths/`
- `GET /api/enrollments/`
- `POST /api/enrollments/`
- `GET /api/progress/`
- `POST /api/progress/`
- `GET /api/organizations/`
- `GET /api/teams/`

Recursos de API globais:

- paginacao por pagina;
- busca com `?search=`;
- ordenacao com `?ordering=`;
- filtros declarados por viewset;
- autenticacao Bearer JWT.
