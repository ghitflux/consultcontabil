# SaaS Contábil

> Sistema de gestão completo para escritórios de contabilidade

## 📋 Sobre o Projeto

Sistema SaaS desenvolvido para otimizar a gestão de escritórios contábeis, incluindo:

- 📊 Gestão de Clientes
- 📅 Controle de Obrigações Fiscais
- 💰 Gestão Financeira (Honorários e Recebimentos)
- 📜 Licenças e Certidões
- 📄 Relatórios Personalizados
- 🔔 Notificações Inteligentes
- 👥 Portal do Cliente
- 🔍 Auditoria Completa

## 🏗️ Arquitetura

Monorepo moderno com as seguintes tecnologias:

### Frontend
- **Next.js 16** com App Router
- **HeroUI** como Design System
- **Tailwind v4** (CSS-first)
- **TypeScript** em strict mode
- **Turbopack** para builds ultra-rápidos

### Backend
- **FastAPI** (Python)
- **SQLAlchemy 2** (async)
- **PostgreSQL 16**
- **Alembic** para migrations
- **Pydantic v2** para validação

### Infraestrutura
- **Docker Compose** para desenvolvimento
- **Nginx** como reverse proxy
- **pnpm** workspaces

## 🚀 Quick Start

### Pré-requisitos

```bash
node >= 18.17.0
pnpm >= 8.0.0
python >= 3.11
docker & docker-compose
```

### Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd ContabilConsult

# Instale as dependências
pnpm install

# Configure as variáveis de ambiente
cp .env.example .env

# Inicie o ambiente de desenvolvimento
docker compose -f infra/docker-compose.dev.yml up
```

### Desenvolvimento Local

```bash
# Frontend (Next.js)
pnpm dev:web

# Backend (FastAPI)
pnpm dev:api

# Todos os serviços via Docker
docker compose -f infra/docker-compose.dev.yml up
```

## 📁 Estrutura do Projeto

```
/
├── apps/
│   ├── web/          # Frontend Next.js 16
│   └── api/          # Backend FastAPI
├── packages/         # Pacotes compartilhados
│   ├── types/       # Tipos TypeScript
│   └── contracts/   # Contratos OpenAPI
├── infra/           # Docker & deployment
├── docs/            # Documentação
└── .vscode/         # Configurações VSCode
```

## 🛠️ Scripts Disponíveis

```bash
pnpm dev              # Inicia todos os workspaces em modo dev
pnpm build            # Build de produção
pnpm lint             # Executa linters
pnpm type-check       # Verifica tipos TypeScript
pnpm test             # Executa testes
pnpm format           # Formata código com Prettier
pnpm clean            # Limpa build artifacts
```

## 📚 Documentação

- [PRD Completo](./docs/PRD.md)
- [Guia de Desenvolvimento](./docs/DEVELOPMENT.md)
- [Arquitetura](./docs/ARCHITECTURE.md) _(em breve)_
- [API Documentation](./docs/API.md) _(em breve)_
- [Database Schema](./docs/DATABASE.md) _(em breve)_

## 🔐 Segurança

- JWT authentication
- RBAC (Role-Based Access Control)
- Auditoria completa de ações
- HTTPS obrigatório em produção
- Rate limiting
- CORS configurado

## 🧪 Testes

```bash
# Frontend tests
pnpm --filter web test

# Backend tests
cd apps/api
pytest

# Coverage report
pnpm test:coverage
```

## 🚢 Deploy

```bash
# Staging
docker compose -f infra/docker-compose.stage.yml up -d

# Production
docker compose -f infra/docker-compose.prod.yml up -d
```

## 🤝 Contribuindo

1. Siga o [guia de desenvolvimento](./docs/DEVELOPMENT.md)
2. Use Conventional Commits
3. Todos os PRs devem passar nos testes
4. Cobertura de testes mínima: 80%

## 📄 Licença

Proprietary - Todos os direitos reservados

## 👥 Time

Desenvolvido por Contabil Consult

---

**Status**: 🚧 Em Desenvolvimento - Marco 1 (Fundação)

_Última atualização: 2025-10-30_
