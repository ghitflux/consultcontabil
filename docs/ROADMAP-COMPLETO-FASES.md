# 🗺️ ROADMAP COMPLETO - TODAS AS FASES

**Projeto**: ContabilConsult - Sistema de Gestão Contábil
**Data**: 11/11/2025
**Status Geral**: 70% Completo

---

## 📊 VISÃO GERAL DO PROJETO

### **Progresso Atual**
```
█████████████████████░░░░░░░░░░ 70%

✅ Fase 1: Backend Clientes + Configurações (COMPLETA)
⏳ Fase 2: Frontend Configurações (50% - Infra pronta)
⏳ Fase 3: Corrigir Gaps Obrigações (0%)
⏳ Fase 4: Relatórios Frontend (0%)
⏳ Fase 5: Testes Automatizados (0%)
⏳ Fase 6: Melhorias de Autenticação (0%)
⏳ Fase 7: Portal do Cliente (30%)
⏳ Fase 8: Dashboards e Analytics (0%)
⏳ Fase 9: Notificações e Alertas (0%)
⏳ Fase 10: Integrações Externas (0%)
⏳ Fase 11: Performance e Scale (0%)
```

### **Módulos por Status**

| Módulo | Backend | Frontend | Status |
|--------|---------|----------|--------|
| Autenticação | ✅ 100% | ✅ 100% | ✅ Completo |
| Clientes | ✅ 100% | ✅ 100% | ✅ Completo |
| Usuários/Config | ✅ 100% | 🟡 50% | 🟡 Parcial |
| Obrigações | 🟡 90% | 🟡 85% | 🟡 Parcial |
| Licenças | ✅ 95% | ✅ 95% | ✅ Completo |
| Financeiro | 🟡 85% | 🟡 85% | 🟡 Parcial |
| Relatórios | ✅ 100% | ⏳ 0% | 🔴 Bloqueado |
| Portal Cliente | 🟡 60% | 🟡 30% | 🟡 Parcial |
| Atividades | ⏳ 10% | ⏳ 10% | 🔴 Não Iniciado |

---

## ✅ FASE 1: BACKEND CLIENTES + CONFIGURAÇÕES (COMPLETA)

**Status**: ✅ 100% Concluída
**Data**: 11/11/2025
**Duração**: 4 horas

### O que foi entregue:
- ✅ Migration `client_users` (N:N)
- ✅ Modelo `ClientUser` com `ClientAccessLevel`
- ✅ ClientService - Criação automática de usuário
- ✅ UserService - CRUD completo
- ✅ 6 novos endpoints REST
- ✅ Seeds com 10 usuários realistas
- ✅ Documentação completa

### Arquivos criados/modificados:
- **Criados**: 13 arquivos
- **Modificados**: 10 arquivos
- **Linhas de código**: ~1.200

**Documentação**: Ver [IMPLEMENTACAO-FASE-1-RESUMO.md](IMPLEMENTACAO-FASE-1-RESUMO.md)

---

## 🔄 FASE 2: FRONTEND - MÓDULO DE CONFIGURAÇÕES

**Status**: 🟡 50% Completo (Infra pronta)
**Prioridade**: 🔴 ALTA
**Estimativa**: 3-4 horas
**Dependências**: Fase 1 ✅

### 📋 Tarefas

#### ✅ Concluído (50%)
- [x] Types TypeScript completos
- [x] API client `usersApi` funcional
- [x] Hook `useUsers` com estado
- [x] Componentes `UserRoleChip` e `UserStatusChip`

#### ⏳ Pendente (50%)

**2.1 - Componente UsersTable.tsx** (1.5h)
```tsx
// apps/web/src/components/features/users/UsersTable.tsx
Funcionalidades:
- [ ] Tabela HeroUI com colunas: Nome, Email, Role, Status, Último Login, Ações
- [ ] Filtros: busca (nome/email), role (select), is_active (checkbox)
- [ ] Paginação server-side (integrada com useUsers)
- [ ] Ações por linha:
  - Editar (ícone lápis)
  - Ativar/Desativar (switch)
  - Resetar Senha (ícone chave)
  - Excluir (ícone lixeira, apenas admin)
- [ ] Loading skeleton enquanto carrega
- [ ] Empty state quando não há usuários
- [ ] Responsive (mobile: cards, desktop: table)
```

**2.2 - Componente UserFormModal.tsx** (1h)
```tsx
// apps/web/src/components/features/users/UserFormModal.tsx
Funcionalidades:
- [ ] Modal HeroUI para criar/editar usuário
- [ ] Campos:
  - Nome (input text, required)
  - Email (input email, required)
  - Role (select: admin/func/cliente, required)
  - Senha (input password, apenas criar, required)
  - Confirmar Senha (input password, apenas criar, required)
- [ ] Validações:
  - Email válido
  - Senha mínimo 8 caracteres
  - Senha com letra + número
  - Senhas devem ser iguais
- [ ] Loading state no botão de salvar
- [ ] Feedback de sucesso/erro (toast)
- [ ] Fechar modal após sucesso
```

**2.3 - Componente ResetPasswordModal.tsx** (30min)
```tsx
// apps/web/src/components/features/users/ResetPasswordModal.tsx
Funcionalidades:
- [ ] Modal para resetar senha
- [ ] 2 opções:
  - Gerar senha temporária (checkbox checked por padrão)
  - Definir nova senha (2 campos: senha + confirmar)
- [ ] Mostrar senha temporária gerada em alert
- [ ] Botão copiar senha temporária
- [ ] Loading state
```

**2.4 - Página /configuracoes** (1h)
```tsx
// apps/web/app/(dashboard)/configuracoes/page.tsx
Estrutura:
- [ ] Layout com PageTitle "Configurações"
- [ ] HeroUI Tabs com 3 abas:
  1. Usuários (UsersTable)
  2. Sistema (placeholder por enquanto)
  3. Perfil (dados do usuário logado)
- [ ] Tab Usuários:
  - Botão "Novo Usuário" (abre UserFormModal)
  - UsersTable integrado
- [ ] Tab Sistema:
  - Placeholder com texto "Em breve"
- [ ] Tab Perfil:
  - Card com dados do usuário atual
  - Botão "Alterar Senha"
  - Botão "Editar Perfil"
- [ ] RBAC: apenas admin vê tab Usuários
- [ ] Loading state global
```

### 🎯 Critérios de Aceitação
- [ ] Admin consegue listar todos usuários
- [ ] Admin consegue criar novo usuário
- [ ] Admin consegue editar usuário existente
- [ ] Admin consegue ativar/desativar usuário
- [ ] Admin consegue resetar senha de usuário
- [ ] Senha temporária é mostrada e pode ser copiada
- [ ] Filtros funcionam corretamente
- [ ] Paginação funciona corretamente
- [ ] Usuário comum (func/cliente) não vê tab Usuários
- [ ] Feedback visual para todas ações (loading, sucesso, erro)

### 📦 Entregáveis
```
apps/web/src/components/features/users/
  ├── UsersTable.tsx (novo)
  ├── UserFormModal.tsx (novo)
  ├── ResetPasswordModal.tsx (novo)
  └── UserChips.tsx (existente)

apps/web/app/(dashboard)/
  └── configuracoes/
      └── page.tsx (novo)
```

---

## 🔧 FASE 3: CORRIGIR GAPS DE OBRIGAÇÕES

**Status**: ⏳ 0%
**Prioridade**: 🟡 MÉDIA
**Estimativa**: 8 horas
**Dependências**: Nenhuma

### 📋 Problemas Identificados

**3.1 - Tipos de Obrigações Hardcoded** (2h)
```typescript
Problema:
- Frontend usa lista fixa: DCTFWeb, EFD-Contribuições, ECD, ECF, ISS, FGTS, INSS
- Backend usa tipos dinâmicos via obligation_types table

Solução:
- [ ] Criar endpoint GET /obligation-types
- [ ] Atualizar frontend para buscar tipos dinamicamente
- [ ] Cache de tipos no frontend (localStorage)
- [ ] Fallback para lista hardcoded se API falhar
```

**3.2 - Endpoint /obligations/list Não Documentado** (3h)
```python
Problema:
- Frontend chama GET /obligations/list?month=X&year=Y&category=clients
- Endpoint não existe em obligations.py routes

Solução:
- [ ] Opção 1: Implementar endpoint /obligations/list
      - Retornar estrutura específica para matriz view
      - Filtros: month, year, category (clients/escritorio)

- [ ] Opção 2: Refatorar frontend para usar /obligations com filtros
      - Ajustar frontend para construir matriz localmente
      - Usar endpoint existente com filtros adequados

Recomendação: Opção 1 (melhor performance)
```

**3.3 - Endpoint /obligations/matrix Otimizado** (2h)
```python
# apps/api/app/api/v1/routes/obligations.py

Novo endpoint:
- [ ] GET /obligations/matrix
- [ ] Query params: month, year, category
- [ ] Response: estrutura pré-formatada para matriz
- [ ] Performance: 1 query ao invés de N queries
- [ ] Exemplo de response:
{
  "month": 11,
  "year": 2025,
  "clients": [
    {
      "id": "uuid",
      "name": "Empresa ABC",
      "obligations": {
        "DCTFWEB": { "status": "concluida", "due_date": "2025-11-20", ... },
        "EFD": { "status": "pendente", "due_date": "2025-11-25", ... }
      }
    }
  ]
}
```

**3.4 - Upload de Recibo** (1h)
```typescript
Problema:
- Frontend tenta usar ID composto ${clientId}-${type}
- Backend espera obligation_id UUID

Solução:
- [ ] Criar obrigações automaticamente se não existirem
- [ ] Endpoint POST /obligations/ensure-exists
      - Recebe: client_id, type, month, year
      - Retorna: obligation_id (cria se não existir)
- [ ] Frontend chama ensure-exists antes de upload
```

### 🎯 Critérios de Aceitação
- [ ] Tipos de obrigações vêm do backend
- [ ] Matriz view carrega em < 2 segundos
- [ ] Upload de recibo funciona sem erros
- [ ] Progresso por cliente está correto
- [ ] Filtro de competência funciona

---

## 📊 FASE 4: RELATÓRIOS - FRONTEND COMPLETO

**Status**: ⏳ 0%
**Prioridade**: 🟡 MÉDIA
**Estimativa**: 25 horas
**Dependências**: Backend 100% ✅

### 📋 Tarefas

**4.1 - API Client e Hooks** (3h)
```typescript
Arquivos:
- [ ] apps/web/src/lib/api/endpoints/reports.ts
      - listReportTypes()
      - listTemplates()
      - createTemplate()
      - updateTemplate()
      - deleteTemplate()
      - preview()
      - export()
      - download()
      - getHistory()

- [ ] apps/web/src/hooks/useReports.ts
      - Estado: reports, selectedReport, isLoading, error
      - Operações: fetch, create, update, delete, preview, export
```

**4.2 - Componentes Base** (4h)
```tsx
Componentes:
- [ ] ReportTypeSelector.tsx
      - Dropdown com 11 tipos de relatórios
      - Ícone e descrição por tipo

- [ ] ReportFiltersPanel.tsx
      - Filtros dinâmicos baseados no tipo
      - Date range picker
      - Client selector
      - Custom filters por tipo

- [ ] ReportPreview.tsx
      - Visualização do relatório
      - Tabelas com dados
      - Gráficos (recharts)
      - Botões: Exportar PDF, Exportar CSV
```

**4.3 - Dashboard Executivo** (5h)
```tsx
Página: apps/web/app/(dashboard)/relatorios/page.tsx

Seções:
- [ ] KPIs principais (cards)
      - Total de relatórios gerados
      - Relatórios do mês
      - Tipos mais usados

- [ ] Gráfico de barras: Relatórios por tipo
- [ ] Gráfico de linha: Relatórios ao longo do tempo
- [ ] Tabela: Últimos relatórios gerados
- [ ] Quick actions: Gerar relatório rápido
```

**4.4 - Report Builder** (6h)
```tsx
Componente: ReportBuilder.tsx

Features:
- [ ] Wizard multi-step:
      1. Selecionar tipo
      2. Configurar filtros
      3. Customizar visualização
      4. Preview
      5. Gerar/Salvar template

- [ ] Formulário dinâmico baseado no tipo
- [ ] Preview em tempo real
- [ ] Salvar como template
- [ ] Validações por step
```

**4.5 - Histórico e Templates** (4h)
```tsx
Componentes:

- [ ] ReportHistory.tsx
      - Tabela com histórico
      - Colunas: Nome, Tipo, Data, Status, Ações
      - Filtros: tipo, data, status
      - Ações: Download, Re-gerar, Excluir

- [ ] ReportTemplates.tsx
      - Cards com templates salvos
      - Templates do sistema (read-only)
      - Templates do usuário (editar/excluir)
      - Botão: Usar template
```

**4.6 - Portal do Cliente - Relatórios** (3h)
```tsx
Página: apps/web/app/portal/relatorios/page.tsx

Features:
- [ ] Lista de relatórios disponíveis (filtrado por cliente)
- [ ] Download de relatórios
- [ ] Visualização inline (PDF.js)
- [ ] Filtros: tipo, data
- [ ] Apenas visualização (não gera relatórios)
```

### 🎯 Critérios de Aceitação
- [ ] Admin/Func consegue gerar todos os 11 tipos de relatórios
- [ ] Preview funciona antes de exportar
- [ ] Export PDF e CSV funciona
- [ ] Templates podem ser salvos e reutilizados
- [ ] Histórico mostra todos relatórios gerados
- [ ] Cliente consegue ver/baixar seus relatórios
- [ ] Gráficos são interativos e responsivos

### 📦 Dependências Externas
```bash
# Instalar no frontend:
pnpm add recharts date-fns
pnpm add @types/recharts -D
```

---

## 🧪 FASE 5: TESTES AUTOMATIZADOS

**Status**: ⏳ 0%
**Prioridade**: 🔴 ALTA (Crítico para produção)
**Estimativa**: 24 horas
**Dependências**: Todas features principais completas

### 📋 Tarefas

**5.1 - Backend: Testes Unitários (pytest)** (10h)
```python
Estrutura:
apps/api/tests/
  ├── unit/
  │   ├── models/
  │   │   ├── test_user.py
  │   │   ├── test_client.py
  │   │   ├── test_client_user.py
  │   │   └── ...
  │   ├── services/
  │   │   ├── test_client_service.py
  │   │   ├── test_user_service.py
  │   │   ├── test_obligation_service.py
  │   │   └── ...
  │   ├── repositories/
  │   │   └── test_user_repository.py
  │   └── core/
  │       └── test_security.py

Cobertura mínima: 80%

Testes por service:
- [ ] ClientService (15 tests)
      - test_create_client_with_user
      - test_create_client_without_user
      - test_create_client_duplicate_cnpj
      - test_create_client_duplicate_email
      - test_temporary_password_generation
      - ...

- [ ] UserService (12 tests)
      - test_create_user
      - test_update_user
      - test_activate_deactivate
      - test_reset_password
      - test_link_to_client
      - ...

- [ ] ObligationService (10 tests)
- [ ] LicenseService (8 tests)
- [ ] FinanceService (8 tests)
```

**5.2 - Frontend: Testes Unitários (Jest + RTL)** (8h)
```typescript
Estrutura:
apps/web/__tests__/
  ├── components/
  │   ├── users/
  │   │   ├── UserChips.test.tsx
  │   │   ├── UsersTable.test.tsx
  │   │   └── UserFormModal.test.tsx
  │   └── ...
  ├── hooks/
  │   ├── useUsers.test.ts
  │   ├── useClients.test.ts
  │   └── ...
  └── lib/
      └── api/
          └── endpoints/
              ├── users.test.ts
              └── ...

Cobertura mínima: 70%

Testes por componente:
- [ ] UserChips (5 tests)
      - renders role chip correctly
      - renders status chip correctly
      - applies correct colors

- [ ] UsersTable (15 tests)
      - renders empty state
      - renders users list
      - filters work correctly
      - pagination works
      - actions buttons trigger correctly

- [ ] useUsers hook (10 tests)
      - fetchUsers works
      - createUser works
      - error handling works
      - loading states work
```

**5.3 - E2E: Testes de Fluxo (Playwright)** (6h)
```typescript
Estrutura:
apps/web/e2e/
  ├── auth.spec.ts
  ├── clients.spec.ts
  ├── users.spec.ts
  ├── obligations.spec.ts
  └── ...

Fluxos críticos:
- [ ] auth.spec.ts (5 tests)
      - Login com credenciais válidas
      - Login com credenciais inválidas
      - Logout
      - Refresh token automático
      - Session expiration

- [ ] clients.spec.ts (8 tests)
      - Criar cliente sem usuário
      - Criar cliente com usuário
      - Editar cliente
      - Buscar cliente
      - Filtrar clientes
      - Paginação

- [ ] users.spec.ts (10 tests)
      - Criar usuário
      - Editar usuário
      - Ativar/Desativar
      - Resetar senha
      - Copiar senha temporária
      - Listar com filtros
```

### 🎯 Critérios de Aceitação
- [ ] Cobertura backend ≥ 80%
- [ ] Cobertura frontend ≥ 70%
- [ ] Todos testes E2E passam
- [ ] CI/CD executa testes automaticamente
- [ ] Relatório de cobertura gerado

### 📦 Configuração
```bash
# Backend
cd apps/api
pip install pytest pytest-cov pytest-asyncio httpx

# Frontend
cd apps/web
pnpm add -D @testing-library/react @testing-library/jest-dom
pnpm add -D @playwright/test
```

---

## 🔐 FASE 6: MELHORIAS DE AUTENTICAÇÃO

**Status**: ⏳ 0%
**Prioridade**: 🟡 MÉDIA
**Estimativa**: 15 horas
**Dependências**: Fase 1 ✅

### 📋 Tarefas

**6.1 - Reset de Senha via Email** (5h)

**Backend:**
```python
# apps/api/app/api/v1/routes/auth.py

Novos endpoints:
- [ ] POST /auth/forgot-password
      - Body: { email }
      - Gera token único (UUID + timestamp)
      - Salva token no Redis (TTL 1 hora)
      - Envia email com link
      - Response: { success, message }

- [ ] POST /auth/reset-password
      - Body: { token, new_password }
      - Valida token
      - Atualiza senha
      - Invalida token
      - Response: { success, message }

Modelo:
- [ ] Tabela password_reset_tokens
      - id, user_id, token, expires_at, used_at

Integração:
- [ ] Resend ou SendGrid para emails
- [ ] Template HTML de email
```

**Frontend:**
```tsx
Páginas:
- [ ] app/(auth)/forgot-password/page.tsx
      - Form com email
      - Botão "Enviar link de reset"
      - Mensagem de sucesso

- [ ] app/(auth)/reset-password/[token]/page.tsx
      - Form com senha + confirmar senha
      - Validação de senha forte
      - Mensagem de sucesso
      - Redirect para login
```

**6.2 - Verificação de Email** (4h)

**Backend:**
```python
Novos endpoints:
- [ ] POST /auth/send-verification
      - Envia email com link de verificação
      - Token com TTL 24 horas

- [ ] GET /auth/verify-email/{token}
      - Valida token
      - Marca is_verified = True
      - Redirect para login
```

**Frontend:**
```tsx
- [ ] Banner na dashboard para usuários não verificados
- [ ] Botão "Reenviar email de verificação"
- [ ] Página de sucesso após verificação
```

**6.3 - Logs de Atividade** (3h)

**Backend:**
```python
# apps/api/app/db/models/activity_log.py

Novo modelo:
- [ ] ActivityLog
      - user_id, action, ip_address, user_agent
      - resource_type, resource_id
      - details (JSONB)
      - created_at

Eventos para logar:
- [ ] Login/Logout
- [ ] Criação de cliente
- [ ] Modificação de dados sensíveis
- [ ] Reset de senha
- [ ] Mudança de role

Endpoint:
- [ ] GET /users/me/activity
      - Lista atividades do usuário logado
      - Filtros: action, date_range
      - Paginação
```

**Frontend:**
```tsx
- [ ] Tab "Atividade Recente" na página /configuracoes
- [ ] Tabela com últimas 50 atividades
- [ ] Filtros por tipo de ação
```

**6.4 - 2FA (Opcional)** (3h)

**Backend:**
```python
Novo modelo:
- [ ] TwoFactorAuth
      - user_id, secret, backup_codes, enabled_at

Endpoints:
- [ ] POST /auth/2fa/enable
      - Gera secret TOTP
      - Retorna QR code

- [ ] POST /auth/2fa/verify
      - Valida código de 6 dígitos
      - Ativa 2FA

- [ ] POST /auth/2fa/disable
      - Desativa 2FA

- [ ] POST /auth/login/2fa
      - Valida 2FA após login normal
```

**Frontend:**
```tsx
- [ ] Modal para ativar 2FA
- [ ] QR code display
- [ ] Input de 6 dígitos
- [ ] Backup codes display
- [ ] Página de login com 2FA
```

### 🎯 Critérios de Aceitação
- [ ] Reset de senha via email funciona
- [ ] Email de verificação é enviado e funciona
- [ ] Atividades são logadas corretamente
- [ ] 2FA funciona (opcional)
- [ ] Templates de email são profissionais

---

## 👥 FASE 7: PORTAL DO CLIENTE COMPLETO

**Status**: 🟡 30% (estrutura básica existe)
**Prioridade**: 🟡 MÉDIA
**Estimativa**: 30 horas
**Dependências**: Fase 3 ✅, Fase 4 ✅

### 📋 Tarefas

**7.1 - Refinar UX/UI** (8h)
```tsx
Páginas para refinar:
- [ ] app/portal/layout.tsx
      - Sidebar específica para cliente
      - Logo do cliente
      - Menu simplificado

- [ ] app/portal/page.tsx (Dashboard)
      - Cards com resumo
      - Próximas obrigações
      - Status de licenças
      - Últimas transações
      - Gráficos simples
```

**7.2 - Notificações Push** (6h)

**Backend:**
```python
# apps/api/app/services/notification_service.py

Tipos de notificação:
- [ ] Obrigação próxima do vencimento (3 dias antes)
- [ ] Licença vencendo (15 dias antes)
- [ ] Honorários a vencer
- [ ] Documento pendente

Implementação:
- [ ] Job agendado (APScheduler)
- [ ] Notifica usuários via:
      - In-app notifications
      - Email (opcional)
      - WhatsApp (opcional)

Endpoint:
- [ ] GET /notifications
- [ ] PATCH /notifications/{id}/read
- [ ] DELETE /notifications/{id}
```

**Frontend:**
```tsx
- [ ] NotificationBell component
      - Badge com contador
      - Dropdown com lista
      - Mark as read
      - Clear all

- [ ] Página de notificações
- [ ] Som/vibração em nova notificação
```

**7.3 - Upload de Documentos** (8h)

**Backend:**
```python
# apps/api/app/api/v1/routes/documents.py

Novo módulo:
- [ ] Modelo Document
      - client_id, user_id, category, filename
      - file_path, file_size, mime_type
      - description, uploaded_at

Endpoints:
- [ ] POST /documents/upload
      - Multipart file upload
      - Validações: tamanho, tipo
      - S3 ou storage local

- [ ] GET /documents
      - Lista documentos do cliente
      - Filtros: category, date

- [ ] GET /documents/{id}/download
      - Download com autenticação

- [ ] DELETE /documents/{id}
```

**Frontend:**
```tsx
Página: app/portal/documentos/page.tsx

Features:
- [ ] Drag & drop upload
- [ ] Progress bar
- [ ] Lista de documentos
- [ ] Preview (PDF inline)
- [ ] Download
- [ ] Categorias: Fiscal, Contábil, Pessoal, Outros
```

**7.4 - Sistema de Solicitações/Tickets** (8h)

**Backend:**
```python
# apps/api/app/db/models/ticket.py

Novo modelo:
- [ ] Ticket
      - client_id, user_id, assigned_to
      - subject, description, priority, status
      - category (dúvida, documento, urgente)
      - created_at, updated_at, closed_at

- [ ] TicketMessage
      - ticket_id, user_id, message
      - attachments (JSONB)
      - created_at

Endpoints:
- [ ] POST /tickets
- [ ] GET /tickets
- [ ] GET /tickets/{id}
- [ ] POST /tickets/{id}/messages
- [ ] PATCH /tickets/{id}/close
```

**Frontend:**
```tsx
Páginas:
- [ ] app/portal/solicitacoes/page.tsx
      - Botão "Nova Solicitação"
      - Lista de tickets
      - Status badges

- [ ] app/portal/solicitacoes/[id]/page.tsx
      - Thread de mensagens
      - Form para responder
      - Upload de anexos
      - Botão fechar ticket
```

### 🎯 Critérios de Aceitação
- [ ] Cliente vê apenas seus dados
- [ ] Notificações funcionam em tempo real
- [ ] Upload de documentos é seguro
- [ ] Cliente consegue abrir tickets
- [ ] Comunicação bidirecional funciona
- [ ] UX é intuitiva para não-técnicos

---

## 📈 FASE 8: DASHBOARDS E ANALYTICS

**Status**: ⏳ 0%
**Prioridade**: 🟢 BAIXA
**Estimativa**: 40 horas
**Dependências**: Todas features principais ✅

### 📋 Tarefas

**8.1 - Dashboard Executivo** (15h)
```tsx
Página: app/(dashboard)/analytics/page.tsx

KPIs principais:
- [ ] Total de clientes (ativos/inativos)
- [ ] Receita mensal (real vs previsto)
- [ ] Taxa de cumprimento de obrigações
- [ ] Taxa de renovação de licenças
- [ ] Tempo médio de resposta
- [ ] Satisfação do cliente (NPS)

Gráficos:
- [ ] Linha: Receita ao longo do tempo (12 meses)
- [ ] Barra: Clientes por regime tributário
- [ ] Pizza: Distribuição por tipo de empresa
- [ ] Área: Obrigações cumpridas vs atrasadas
- [ ] Heatmap: Obrigações por cliente/mês
- [ ] Funil: Pipeline de clientes
```

**8.2 - Dashboards por Módulo** (10h)
```tsx
Dashboards específicos:

- [ ] Dashboard Financeiro
      - Receita por cliente
      - Inadimplência
      - Aging report visual
      - Projeções

- [ ] Dashboard Obrigações
      - Taxa de cumprimento
      - Obrigações mais atrasadas
      - Performance por funcionário
      - Trending

- [ ] Dashboard Clientes
      - Churn rate
      - Lifetime value
      - Novos clientes por mês
      - Satisfação
```

**8.3 - Relatórios Customizáveis** (10h)
```tsx
Report Builder avançado:

- [ ] Drag & drop de métricas
- [ ] Filtros dinâmicos
- [ ] Múltiplos tipos de gráficos
- [ ] Exportar dashboard como PDF
- [ ] Salvar dashboards customizados
- [ ] Compartilhar via link
```

**8.4 - Alertas Inteligentes** (5h)
```python
Backend - Sistema de alertas:

- [ ] Detecta anomalias:
      - Queda brusca na receita
      - Aumento de obrigações atrasadas
      - Clientes inativos por > 30 dias

- [ ] Envia alertas para admin
- [ ] Dashboard de alertas
```

### 🎯 Critérios de Aceitação
- [ ] KPIs são calculados corretamente
- [ ] Gráficos são interativos
- [ ] Performance < 3s para carregar dashboard
- [ ] Dashboards podem ser exportados
- [ ] Alertas são acionados corretamente

---

## 🔔 FASE 9: NOTIFICAÇÕES E ALERTAS

**Status**: ⏳ 0%
**Prioridade**: 🟡 MÉDIA
**Estimativa**: 30 horas
**Dependências**: Fase 7 ✅

### 📋 Tarefas

**9.1 - Sistema de Notificações In-App** (10h)

**Backend:**
```python
Implementação completa:
- [ ] WebSocket server (FastAPI WebSocket)
- [ ] Pub/Sub pattern
- [ ] Notificações persistentes em DB
- [ ] Marcação de lida/não lida
- [ ] Agrupamento de notificações
```

**Frontend:**
```tsx
- [ ] NotificationProvider (Context)
- [ ] WebSocket client
- [ ] Toast notifications
- [ ] NotificationCenter component
- [ ] Som/vibração
- [ ] Badge em tempo real
```

**9.2 - Email Notifications** (8h)

**Integração Resend/SendGrid:**
```python
Templates de email:
- [ ] Bem-vindo (novo cliente)
- [ ] Credenciais de acesso
- [ ] Obrigação vencendo
- [ ] Licença vencendo
- [ ] Honorários a vencer
- [ ] Documento pendente
- [ ] Ticket respondido
- [ ] Reset de senha

Features:
- [ ] HTML templates responsivos
- [ ] Variáveis dinâmicas
- [ ] Tracking de abertura
- [ ] Unsubscribe link
```

**9.3 - WhatsApp Integration (Opcional)** (12h)

**Twilio API:**
```python
Implementação:
- [ ] Integração com Twilio
- [ ] Templates de mensagem WhatsApp
- [ ] Opt-in/opt-out
- [ ] Rate limiting
- [ ] Custo por mensagem

Mensagens:
- [ ] Obrigação vencendo amanhã
- [ ] Licença vencida
- [ ] Documento urgente
- [ ] Honorários em atraso
```

### 🎯 Critérios de Aceitação
- [ ] Notificações in-app funcionam em tempo real
- [ ] Emails são enviados corretamente
- [ ] WhatsApp funciona (se implementado)
- [ ] Usuário pode configurar preferências
- [ ] Não há spam de notificações

---

## 🔌 FASE 10: INTEGRAÇÕES EXTERNAS

**Status**: ⏳ 0%
**Prioridade**: 🟢 BAIXA (Nice to have)
**Estimativa**: 60 horas
**Dependências**: Sistema estável

### 📋 Tarefas

**10.1 - API Receita Federal** (15h)
```python
Consultas:
- [ ] Validação de CNPJ
- [ ] Consulta situação cadastral
- [ ] Download de certidões
- [ ] Consulta débitos

Implementação:
- [ ] Rate limiting
- [ ] Cache de resultados (24h)
- [ ] Retry automático
- [ ] Error handling
```

**10.2 - API Sefaz** (20h)
```python
Funcionalidades:
- [ ] Consulta NFe
- [ ] Download XML
- [ ] Validação de chave de acesso
- [ ] Manifestação do destinatário

Desafios:
- [ ] Múltiplas Sefaz estaduais
- [ ] Certificado digital
- [ ] Web services SOAP
```

**10.3 - Sistema de Pagamentos** (15h)
```python
Stripe ou PagSeguro:
- [ ] Checkout de honorários
- [ ] Boleto bancário
- [ ] Cartão de crédito
- [ ] PIX
- [ ] Webhooks
- [ ] Conciliação automática
```

**10.4 - Integração Bancária** (10h)
```python
Open Banking:
- [ ] Consulta de extratos
- [ ] Conciliação automática
- [ ] Previsão de fluxo de caixa
```

### 🎯 Critérios de Aceitação
- [ ] Validação de CNPJ é instantânea
- [ ] NFes são baixadas corretamente
- [ ] Pagamentos são processados
- [ ] Webhooks são tratados
- [ ] Dados bancários são sincronizados

---

## ⚡ FASE 11: PERFORMANCE E SCALE

**Status**: ⏳ 0%
**Prioridade**: 🟡 MÉDIA (Para crescimento)
**Estimativa**: 40 horas
**Dependências**: Sistema em produção

### 📋 Tarefas

**11.1 - Caching (Redis)** (10h)
```python
Implementação:
- [ ] Redis setup (Docker)
- [ ] Cache de queries frequentes:
      - Lista de clientes
      - Tipos de obrigações
      - KPIs do dashboard
- [ ] TTL por tipo de dado
- [ ] Invalidação de cache
- [ ] Cache warming
```

**11.2 - Background Jobs (Celery)** (12h)
```python
Tasks assíncronas:
- [ ] Geração de relatórios
- [ ] Envio de emails em massa
- [ ] Processamento de uploads
- [ ] Cálculo de KPIs
- [ ] Backup automático

Setup:
- [ ] Celery + Redis
- [ ] Task queues por prioridade
- [ ] Retry logic
- [ ] Monitoring (Flower)
```

**11.3 - Database Optimization** (10h)
```sql
Otimizações:
- [ ] Análise de slow queries
- [ ] Índices compostos
- [ ] Materialized views para KPIs
- [ ] Particionamento de tabelas grandes
- [ ] VACUUM e ANALYZE automático
- [ ] Connection pooling tuning
```

**11.4 - CDN e Assets** (8h)
```typescript
Frontend optimization:
- [ ] CloudFront ou Cloudflare
- [ ] Image optimization
- [ ] Code splitting avançado
- [ ] Lazy loading de rotas
- [ ] Service Worker (PWA)
- [ ] Compression (Brotli)
```

### 🎯 Critérios de Aceitação
- [ ] Cache hit rate > 80%
- [ ] Relatórios grandes não bloqueiam API
- [ ] Queries < 100ms (P95)
- [ ] Frontend carrega < 2s (3G)
- [ ] Suporta 1000+ usuários simultâneos

---

## 📊 RESUMO POR PRIORIDADE

### 🔴 PRIORIDADE ALTA (Crítico)
```
Fase 2: Frontend Configurações (3-4h)
  └─ Completar UI de gerenciamento de usuários

Fase 5: Testes Automatizados (24h)
  └─ Cobertura mínima para produção
```

### 🟡 PRIORIDADE MÉDIA (Importante)
```
Fase 3: Corrigir Gaps Obrigações (8h)
  └─ Sincronizar frontend/backend

Fase 4: Relatórios Frontend (25h)
  └─ Feature core do sistema

Fase 6: Melhorias de Autenticação (15h)
  └─ Segurança e UX

Fase 7: Portal do Cliente (30h)
  └─ Diferencial de mercado

Fase 9: Notificações e Alertas (30h)
  └─ Engajamento de usuários

Fase 11: Performance e Scale (40h)
  └─ Preparar para crescimento
```

### 🟢 PRIORIDADE BAIXA (Nice to have)
```
Fase 8: Dashboards e Analytics (40h)
  └─ Insights avançados

Fase 10: Integrações Externas (60h)
  └─ Automação avançada
```

---

## 📅 CRONOGRAMA SUGERIDO

### **Sprint 1 (1 semana - 40h)**
- ✅ Fase 1: Backend Clientes + Config (COMPLETA)
- ⏳ Fase 2: Frontend Configurações (4h)
- ⏳ Fase 3: Gaps Obrigações (8h)
- ⏳ Fase 4: Relatórios Frontend (25h)
- **Entrega**: Sistema completo para MVP

### **Sprint 2 (1 semana - 40h)**
- ⏳ Fase 5: Testes Automatizados (24h)
- ⏳ Fase 6: Melhorias Auth (15h)
- **Entrega**: Sistema testado e seguro

### **Sprint 3 (2 semanas - 80h)**
- ⏳ Fase 7: Portal do Cliente (30h)
- ⏳ Fase 9: Notificações (30h)
- ⏳ Fase 11: Performance (20h)
- **Entrega**: Sistema production-ready

### **Sprint 4 (2 semanas - 80h)**
- ⏳ Fase 8: Dashboards (40h)
- ⏳ Fase 11: Performance final (20h)
- ⏳ Fase 10: Integrações (20h início)
- **Entrega**: Sistema completo com analytics

### **Sprint 5+ (Ongoing)**
- ⏳ Fase 10: Integrações restantes (40h)
- ⏳ Melhorias contínuas
- ⏳ Novas features baseadas em feedback

---

## 🎯 CRITÉRIOS DE SUCESSO GLOBAL

### MVP (Mínimo Viável)
- [ ] Autenticação funcional
- [ ] CRUD de clientes completo
- [ ] Gestão de usuários funcional
- [ ] Obrigações sincronizadas
- [ ] Licenças funcionais
- [ ] Financeiro operacional
- [ ] Relatórios básicos funcionais

### Produção (Launch)
- [ ] Testes automatizados (≥80% backend, ≥70% frontend)
- [ ] Segurança reforçada (reset senha, logs)
- [ ] Performance otimizada (< 3s dashboards)
- [ ] Portal do cliente funcional
- [ ] Notificações funcionando
- [ ] Documentação completa

### Escala (Growth)
- [ ] Dashboards avançados
- [ ] Integrações externas
- [ ] Caching implementado
- [ ] Background jobs
- [ ] CDN configurado
- [ ] Suporta 1000+ usuários

---

## 📝 NOTAS IMPORTANTES

### **Decisões Arquiteturais Pendentes**
1. **Email Service**: Resend (mais moderno) vs SendGrid (mais features)
2. **Caching**: Redis standalone vs Redis Cluster
3. **Background Jobs**: Celery vs APScheduler vs RQ
4. **Frontend State**: Manter hooks locais vs Zustand/Redux
5. **File Storage**: Local vs S3 vs Cloudflare R2

### **Riscos Identificados**
- 🔴 **Alto**: Falta de testes pode causar bugs em produção
- 🟡 **Médio**: Gaps de obrigações podem confundir usuários
- 🟡 **Médio**: Performance sem cache pode ser lenta com muitos dados
- 🟢 **Baixo**: Integrações externas podem ter instabilidade

### **Melhorias Futuras (Backlog)**
- [ ] Mobile app (React Native)
- [ ] Assinatura eletrônica de documentos
- [ ] IA para detecção de anomalias
- [ ] Chatbot de atendimento
- [ ] Integração com contabilidade (SPED)
- [ ] Multi-tenancy (SaaS)

---

## 🏆 CONCLUSÃO

**Total Estimado**: ~305 horas restantes
**Progresso Atual**: 70% completo
**MVP**: ~80 horas (Sprints 1-2)
**Produção**: ~165 horas (Sprints 1-3)
**Sistema Completo**: ~305 horas (Sprints 1-5)

**Status**:
```
✅ Backend sólido e production-ready
✅ Frontend 50% completo (infra pronta)
⏳ Testes críticos (precisa urgente)
⏳ Portal cliente (diferencial)
⏳ Performance (escala)
```

**Recomendação**: Priorizar Sprints 1-2 para ter MVP testado e pronto para produção.

---

**Documento atualizado em**: 11/11/2025
**Próxima revisão**: Após cada sprint concluído
