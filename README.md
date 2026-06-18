# RoboticaHub Brasil

LMS brasileiro de robotica educacional e competitiva para alunos, professores, mentores, equipes, escolas e organizacoes.

## Stack

- Backend: Python, Django, Django REST Framework, Simple JWT, PostgreSQL, Celery, Redis, Swagger/OpenAPI.
- Frontend: React, TypeScript, Vite, React Router, Axios, React Hook Form, Zod.
- Infra: Docker Compose, `.env`, armazenamento local no desenvolvimento e arquitetura preparada para S3/R2.

## Estrutura

```text
roboticahub-brasil/
  backend/
    config/
    accounts/
    organizations/
    teams/                  # fronteira planejada
    courses/
    assessments/            # fase futura
    projects/               # fase futura
    engineering_notebook/   # fase futura
    news/                   # fase futura
    innovations/            # fase futura
    notifications/          # fase futura
    certificates/           # fase futura
    subscriptions/          # fase futura
    integrations/
  frontend/
  docs/
```

## Execucao com Docker

```bash
cp .env.example .env
docker compose up --build
```

Servicos:

- Frontend: http://127.0.0.1:5173
- Backend: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/api/docs/

## Execucao sem Docker

Backend:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r backend/requirements.txt
set USE_SQLITE=true
.venv/Scripts/python backend/manage.py migrate
.venv/Scripts/python backend/manage.py seed_demo
.venv/Scripts/python backend/manage.py runserver 127.0.0.1:8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Credenciais de Desenvolvimento

- Administrador: `admin@roboticahub.com` / `Admin123!`
- Professor: `professor@roboticahub.com` / `Professor123!`
- Mentor: `mentor@roboticahub.com` / `Mentor123!`
- Aluno: `aluno@roboticahub.com` / `Aluno123!`

Use essas senhas apenas em ambiente de desenvolvimento.

## Comandos

```bash
.venv/Scripts/python backend/manage.py makemigrations
.venv/Scripts/python backend/manage.py migrate
.venv/Scripts/python backend/manage.py seed_demo
.venv/Scripts/python -m pytest backend
```

## Endpoints Principais

- `/api/auth/register/`
- `/api/auth/login/`
- `/api/auth/refresh/`
- `/api/auth/me/`
- `/api/users/`
- `/api/organizations/`
- `/api/teams/`
- `/api/learning-paths/`
- `/api/courses/`
- `/api/enrollments/`
- `/api/progress/`

## Decisoes Tecnicas

- Usuario customizado usa e-mail como login.
- JWT foi escolhido para permitir frontend separado e apps futuros.
- Backend aplica permissoes por papel; frontend apenas adapta navegacao.
- `USE_SQLITE=true` facilita testes locais, mas PostgreSQL e o banco oficial.
- Integracoes FIRST/fontes externas com interface isolada e dados simulados no MVP.

## Proximos Passos

1. Completar Fase 2 com fluxo de matricula e progresso pela UI.
2. Implementar quizzes, atividades, entregas e rubricas.
3. Separar apps `teams`, `projects`, `engineering_notebook`, `news` e `certificates` em modelos proprios.
4. Adicionar auditoria administrativa e politicas LGPD detalhadas.
