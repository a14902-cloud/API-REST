# API REST de gestão de tarefas

Projeto baseado na estrutura da API de hotel original. Usa Flask, Flask-RESTful, Flask-SQLAlchemy, SQLite e Flask-JWT-Extended.

## Executar

```bash
pip install -r requirements.txt
python app.py
```

A aplicação cria automaticamente a base de dados SQLite e as tabelas na pasta `instance`.

## Administrador inicial

- Email: `admin@api.pt`
- Password: `admin123`

Esta conta é criada automaticamente na primeira execução. Altera estas credenciais antes de usar a API fora de um exercício local.

## Endpoints

Envia e recebe JSON. Para as rotas de tarefas, inclui o cabeçalho `Authorization: Bearer TOKEN`.

- `POST /registo` — registar com `username`, `email` e `password`. O perfil é sempre `utilizador`.
- `POST /login` — autenticar com `email` e `password`; devolve `access_token`.
- `POST /logout` — terminar a sessão do token atual.
- `POST /tarefas` — criar com `titulo`, `descricao` e `estado` (`Pendente`, `Em curso` ou `Concluída`).
- `GET /tarefas` — listar as próprias tarefas; admin lista todas.
- `GET /tarefas/<id>` — consultar uma tarefa.
- `PUT /tarefas/<id>` — alterar `titulo`, `descricao` e `estado`.
- `DELETE /tarefas/<id>` — eliminar tarefa.

## Testar com Bruno

A coleção Bruno está na pasta `collections/Tarefas`. Abre essa pasta no Bruno, escolhe o ambiente `Local` e inicia a aplicação. Podes registar e autenticar o utilizador de exemplo ou iniciar sessão como admin. Copia o `access_token` devolvido pelo pedido de login para a variável `token` do ambiente `Local`. Depois usa os pedidos de criar/listar/consultar/alterar/eliminar. Se o ID da tarefa não for `1`, atualiza também a variável `tarefa_id` com o ID devolvido ao criar a tarefa.

Um utilizador normal só gere as suas tarefas; o administrador gere todas. A password é comparada como no projeto original, pelo que este exemplo é apenas para aprendizagem e não deve ser publicado como serviço real sem melhorar a proteção das passwords e das credenciais.
