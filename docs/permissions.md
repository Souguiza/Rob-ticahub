# Permissoes

Perfis previstos:

- `student`
- `teacher`
- `mentor`
- `school_manager`
- `org_manager`
- `content_editor`
- `moderator`
- `admin`

Regras da Fase 1:

- Qualquer usuario autenticado pode ver cursos publicados, organizacoes e equipes.
- Alunos nao podem criar cursos.
- Professores, editores, gestores e admins podem criar/editar cursos.
- Mentores e gestores podem criar equipes/organizacoes.
- Listagem geral de usuarios fica restrita a staff/admin.

As proximas fases devem adicionar permissoes por escopo de organizacao, equipe e propriedade do recurso.
