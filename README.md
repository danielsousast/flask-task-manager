# Flask Task Manager

Gerenciador de tarefas com API REST em Flask e uma tela web simples (página única).

## Stack

- Flask 3, Flask-SQLAlchemy, Flask-Migrate (Alembic)
- Pydantic 2 para validação
- SQLite por padrão
- pytest

## Requisitos

- Python 3.9+

## Como rodar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=run.py
flask db upgrade      # cria o banco e aplica as migrations
python run.py
```

Acesse `http://127.0.0.1:5000/`.

## Configuração

Variáveis opcionais (podem ficar em um arquivo `.env`):

| Variável       | Padrão                | Descrição                    |
|----------------|-----------------------|------------------------------|
| `SECRET_KEY`   | —                     | Chave secreta do Flask       |
| `DATABASE_URL` | `sqlite:///tasks.db`  | URL de conexão do banco      |

## API

Base: `/api/tasks`

| Método | Rota             | Descrição                         |
|--------|------------------|-----------------------------------|
| GET    | `/api/tasks/`    | Lista tarefas (mais novas antes)  |
| GET    | `/api/tasks/<id>`| Busca uma tarefa                  |
| POST   | `/api/tasks/`    | Cria uma tarefa                   |
| PATCH  | `/api/tasks/<id>`| Atualiza campos da tarefa         |
| DELETE | `/api/tasks/<id>`| Remove a tarefa                   |
| GET    | `/health`        | Health check                      |

Campos: `title` (3 a 150 caracteres, obrigatório na criação), `description` (opcional), `completed` (booleano, padrão `false`).

Exemplo:

```bash
curl -X POST http://127.0.0.1:5000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar Flask", "description": "Capítulo 1"}'
```

Erros de validação retornam `400` com `{"error": "Validation error", "details": [...]}`; tarefa inexistente retorna `404`.

## Migrations

Depois de alterar um model:

```bash
flask db migrate -m "descrição da mudança"
flask db upgrade
```

## Testes

```bash
python -m pytest
```

Os testes usam um SQLite em memória e não afetam o banco local.

## Estrutura

```
app/
  models/      # modelos SQLAlchemy
  schemas/     # schemas Pydantic
  services/    # regras de acesso a dados
  routes/      # blueprints (API e página)
  templates/   # HTML (Jinja)
  static/      # CSS e JS da tela
migrations/    # migrations Alembic
tests/         # testes pytest
run.py         # ponto de entrada
```
