# Arquitetura

O RoboticaHub Brasil usa uma arquitetura web separada por aplicacoes:

- Backend Django + Django REST Framework, com apps por dominio.
- Frontend React + TypeScript + Vite consumindo exclusivamente a API.
- PostgreSQL como banco principal, Redis para filas/cache e Celery para trabalhos assíncronos.
- Documentacao OpenAPI em `/api/docs/`.

Na Fase 1 os apps ativos sao `accounts`, `organizations`, `courses` e `common`. Os demais dominios ja existem como fronteiras de pastas para evolucao incremental.

## Decisoes

- Usuario customizado por e-mail desde o inicio.
- JWT com refresh token para clientes web/mobile.
- `created_at`, `updated_at`, UUID publico e soft delete em entidades centrais via `TimestampedModel`.
- Permissoes aplicadas no backend por perfil, sem depender do frontend.
- Integracoes externas isoladas em `backend/integrations/`, usando provedores simulados no MVP.
