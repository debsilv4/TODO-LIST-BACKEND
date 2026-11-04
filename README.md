# Todo List Backend

API de gerenciamento de tarefas em desenvolvimento, criada com Python e FastAPI.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- bcrypt

## Como executar

### 1. Criar e ativar o ambiente virtual

No Windows, pelo PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 3. Configurar o banco de dados

Se ainda não existir o arquivo `.env`, copie o modelo:

```powershell
Copy-Item .env.example .env
```

A configuração inicial usa SQLite localmente.

### 4. Iniciar a API

```powershell
python -m uvicorn app.main:app --reload
```

### 5. Abrir a documentação

Acesse:

http://127.0.0.1:8000/docs

## Rotas disponíveis

- `GET /` — verifica se a API está funcionando.
- `POST /usuarios` — cadastra um usuário.

## Exemplo de cadastro

```json
{
  "nome": "Debora",
  "email": "debora@example.com",
  "senha": "senha123"
}
```

A senha é armazenada como hash. A resposta não deve expor a senha nem seu hash.

## Observações

- O arquivo `.env` não deve ser enviado ao Git.
- O banco local `todo_list.db` também não deve ser enviado ao Git.
- Este projeto está em desenvolvimento; o cadastro de usuários não significa que autenticação ou gerenciamento completo de tarefas já estejam implementados.
