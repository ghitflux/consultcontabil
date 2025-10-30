# Infraestrutura Docker - SaaS Contábil

## 📋 Visão Geral

Este diretório contém toda a configuração Docker para o ambiente de desenvolvimento do projeto.

## 🏗️ Arquitetura

### Serviços

1. **PostgreSQL** (porta 5432)
   - Banco de dados principal
   - PostgreSQL 16
   - Volume persistente para dados

2. **FastAPI Backend** (porta 8000)
   - API REST
   - Hot reload ativado
   - Conectado ao PostgreSQL

3. **Next.js Frontend** (porta 3000)
   - Interface do usuário
   - Hot reload com Turbopack
   - Integrado com API

4. **Nginx** (porta 80)
   - Reverse proxy
   - Roteia `/api/*` para FastAPI
   - Roteia `/` para Next.js
   - Suporte a WebSocket

## 🚀 Como Usar

### Iniciar Ambiente

```bash
# Usando script (Linux/Mac)
./infra/scripts/dev-up.sh

# Ou diretamente com docker compose
docker compose -f infra/docker-compose.dev.yml up --build -d
```

### Parar Ambiente

```bash
# Usando script (Linux/Mac)
./infra/scripts/dev-down.sh

# Ou diretamente
docker compose -f infra/docker-compose.dev.yml down

# Para remover volumes também
docker compose -f infra/docker-compose.dev.yml down -v
```

### Ver Logs

```bash
# Todos os serviços
docker compose -f infra/docker-compose.dev.yml logs -f

# Serviço específico
docker compose -f infra/docker-compose.dev.yml logs -f api
docker compose -f infra/docker-compose.dev.yml logs -f web
docker compose -f infra/docker-compose.dev.yml logs -f postgres
docker compose -f infra/docker-compose.dev.yml logs -f nginx
```

## 🔗 URLs de Acesso

Após iniciar o ambiente:

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Nginx (Proxy)**: http://localhost
- **PostgreSQL**: localhost:5432

## 🗃️ Banco de Dados

### Credenciais Padrão

- **Host**: localhost
- **Port**: 5432
- **Database**: contabil_db
- **User**: contabil
- **Password**: contabil123

### Conectar via psql

```bash
docker compose -f infra/docker-compose.dev.yml exec postgres psql -U contabil -d contabil_db
```

### Executar Migrations

```bash
# Dentro do container da API
docker compose -f infra/docker-compose.dev.yml exec api alembic upgrade head

# Criar nova migration
docker compose -f infra/docker-compose.dev.yml exec api alembic revision --autogenerate -m "description"
```

## 🐛 Troubleshooting

### Serviços não iniciam

```bash
# Ver logs
docker compose -f infra/docker-compose.dev.yml logs

# Recriar containers
docker compose -f infra/docker-compose.dev.yml up --build --force-recreate
```

### PostgreSQL não está acessível

```bash
# Verificar se o container está rodando
docker compose -f infra/docker-compose.dev.yml ps

# Verificar health check
docker compose -f infra/docker-compose.dev.yml exec postgres pg_isready -U contabil
```

### Hot reload não funciona

1. Verifique se os volumes estão configurados corretamente
2. No Windows, pode ser necessário ajustar configurações de compartilhamento de arquivos do Docker Desktop
3. Reinicie o container específico

### Limpar tudo e começar do zero

```bash
# Parar e remover tudo
docker compose -f infra/docker-compose.dev.yml down -v

# Remover imagens
docker compose -f infra/docker-compose.dev.yml down --rmi all

# Rebuild
docker compose -f infra/docker-compose.dev.yml up --build
```

## 📦 Volumes

- `contabil_postgres_data`: Dados do PostgreSQL
- `contabil_api_uploads`: Arquivos enviados via API

## 🌐 Rede

Todos os serviços estão na rede `contabil-network`, permitindo comunicação entre eles.

## 🔧 Customização

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto para customizar:

```env
POSTGRES_USER=contabil
POSTGRES_PASSWORD=contabil123
POSTGRES_DB=contabil_db
POSTGRES_PORT=5432
API_PORT=8000
WEB_PORT=3000
NGINX_PORT=80
SECRET_KEY=your-secret-key-here
```

### Adicionar Serviços

Edite `docker-compose.dev.yml` e adicione novos serviços conforme necessário.

## 📝 Notas

- O ambiente está configurado para **desenvolvimento**
- Hot reload está **ativado** em web e api
- Volumes montados permitem edição em tempo real
- Para produção, use `docker-compose.prod.yml` (a ser criado)
