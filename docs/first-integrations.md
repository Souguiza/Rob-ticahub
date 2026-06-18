# Integracoes FIRST e Fontes Externas

O MVP nao faz scraping agressivo, nao armazena credenciais da FIRST e nao copia artigos completos.

Politica inicial:

- Noticias externas devem armazenar titulo, resumo proprio, fonte e URL original.
- A UI deve exibir atribuicao visivel e botao para leitura na fonte oficial.
- Conteudos oficiais devem receber selo adequado somente quando a origem for verificada.
- Integracoes futuras devem implementar a interface `NewsProvider` em `backend/integrations/base.py`.

Aviso obrigatorio:

> Esta e uma plataforma independente de educacao em robotica e nao representa, nao e patrocinada e nao e oficialmente endossada pela FIRST.
