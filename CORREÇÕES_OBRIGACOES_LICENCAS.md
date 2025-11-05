# Correções - Obrigações e Licenças

## Data: 2025-11-05

### Problemas Identificados

1. **Licenças não apareciam no frontend**
   - O arquivo `/apps/web/src/lib/api/endpoints/licenses.ts` não existia
   - O hook `useLicenses` estava tentando importar este arquivo inexistente
   - Isso causava erro ao tentar carregar as licenças

2. **Erro ao gerar obrigações/licenças**
   - O script de seed de licenças (`/apps/api/scripts/seed_licenses.py`) usava um status inexistente: `LicenseStatus.VENCENDO`
   - Os status corretos são: ATIVA, VENCIDA, PENDENTE_RENOVACAO, EM_PROCESSO, CANCELADA, SUSPENSA

### Correções Aplicadas

#### 1. Criado arquivo de API endpoints para licenças

**Arquivo**: `/apps/web/src/lib/api/endpoints/licenses.ts`

Criado arquivo completo com todos os endpoints necessários:
- `list()` - Listar licenças com filtros
- `getById()` - Obter licença por ID
- `create()` - Criar nova licença
- `update()` - Atualizar licença
- `delete()` - Deletar licença
- `renew()` - Renovar licença
- `getEvents()` - Obter histórico de eventos
- `checkExpirations()` - Verificar licenças expirando

#### 2. Corrigido script de seed de licenças

**Arquivo**: `/apps/api/scripts/seed_licenses.py`

**Alteração**: Linha 86
```python
# Antes:
status = LicenseStatus.VENCENDO

# Depois:
status = LicenseStatus.PENDENTE_RENOVACAO
```

### Estrutura da API

#### Backend (FastAPI)

As rotas estão corretamente registradas em `/apps/api/app/api/v1/router.py`:
- `/api/v1/obligations` - Obrigações
- `/api/v1/licenses` - Licenças

#### Frontend (Next.js)

Estrutura de arquivos:
- **Páginas**:
  - `/apps/web/app/(dashboard)/obrigacoes/page.tsx` - Página de obrigações
  - `/apps/web/app/(dashboard)/licencas/page.tsx` - Página de licenças

- **Hooks**:
  - `/apps/web/src/hooks/useObligations.ts` - Hook de obrigações
  - `/apps/web/src/hooks/useLicenses.ts` - Hook de licenças

- **API Endpoints**:
  - `/apps/web/src/lib/api/endpoints/licenses.ts` - ✅ CRIADO
  - Hook de obrigações usa fetch direto (não precisa de arquivo separado)

- **Types**:
  - `/apps/web/src/types/obligation.ts` - Types de obrigações
  - `/apps/web/src/types/license.ts` - Types de licenças

### Como Testar

1. **Verificar se a API está rodando**:
   ```bash
   cd apps/api
   venv/Scripts/uvicorn.exe app.main:app --reload
   ```

2. **Rodar seeds (se necessário)**:
   ```bash
   # Seed de tipos de obrigações
   venv/Scripts/python.exe -m scripts.seed_obligation_types

   # Seed de clientes (necessário antes de licenças)
   venv/Scripts/python.exe -m scripts.seed_clients

   # Seed de licenças
   venv/Scripts/python.exe -m scripts.seed_licenses
   ```

3. **Iniciar o frontend**:
   ```bash
   cd apps/web
   pnpm dev
   ```

4. **Acessar as páginas**:
   - Obrigações: http://localhost:3000/obrigacoes
   - Licenças: http://localhost:3000/licencas

### Próximos Passos

Se as obrigações/licenças ainda não aparecerem:

1. Verificar se o backend está rodando
2. Verificar se as migrations foram aplicadas:
   ```bash
   venv/Scripts/alembic.exe upgrade head
   ```
3. Verificar se há dados na base executando os scripts de seed
4. Verificar o console do navegador para erros de API
5. Verificar logs do backend para erros de SQL/autenticação

### Arquivos Modificados

- ✅ **CRIADO**: `/apps/web/src/lib/api/endpoints/licenses.ts`
- ✅ **MODIFICADO**: `/apps/api/scripts/seed_licenses.py`

### Status dos Componentes

| Componente | Status | Observação |
|------------|--------|------------|
| API - Obrigações | ✅ OK | Rotas e endpoints configurados |
| API - Licenças | ✅ OK | Rotas e endpoints configurados |
| Frontend - Obrigações | ✅ OK | Página e hooks funcionando |
| Frontend - Licenças | ✅ OK | Arquivo de endpoints criado |
| Seeds - Obrigações | ✅ OK | Script correto |
| Seeds - Licenças | ✅ OK | Script corrigido |
