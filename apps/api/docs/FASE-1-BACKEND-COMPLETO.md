# FASE 1 - BACKEND COMPLETO ✅

**Status**: 100% Concluído
**Data**: 11/11/2025
**Duração**: ~4 horas

---

## 📋 RESUMO EXECUTIVO

Implementação completa do sistema de gestão de usuários e relacionamento Cliente ↔ Usuário no backend. Agora, ao criar um cliente, o sistema automaticamente cria um usuário com role CLIENTE e estabelece o relacionamento com nível de acesso OWNER.

---

## 🎯 OBJETIVOS ALCANÇADOS

### 1. **Sistema de Relacionamento Cliente ↔ Usuário**
- ✅ Relacionamento N:N entre `clients` e `users`
- ✅ 3 níveis de acesso: OWNER, MANAGER, VIEWER
- ✅ Campo `primary_client_id` para acesso rápido

### 2. **Criação Automática de Usuário**
- ✅ Ao criar cliente, cria usuário automaticamente (opcional)
- ✅ Gera senha temporária segura
- ✅ Retorna credenciais na resposta
- ✅ Valida emails duplicados

### 3. **CRUD Completo de Usuários**
- ✅ Listar com filtros (query, role, is_active)
- ✅ Criar, editar, ativar, desativar usuário
- ✅ Reset de senha (admin)
- ✅ Vincular usuário a cliente

### 4. **Seeds Realistas**
- ✅ 10 usuários diversos (2 admins, 3 funcs, 5 clientes)
- ✅ Dados realistas para demonstração

---

## 🗄️ DATABASE SCHEMA

### Tabela: `client_users`
```sql
CREATE TABLE client_users (
    id UUID PRIMARY KEY,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    access_level client_access_level NOT NULL DEFAULT 'VIEWER',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    CONSTRAINT uq_client_users_client_user UNIQUE (client_id, user_id)
);

CREATE INDEX ix_client_users_client_id ON client_users(client_id);
CREATE INDEX ix_client_users_user_id ON client_users(user_id);
```

### Enum: `client_access_level`
```sql
CREATE TYPE client_access_level AS ENUM ('OWNER', 'MANAGER', 'VIEWER');
```

### Alteração: `users` table
```sql
ALTER TABLE users ADD COLUMN primary_client_id UUID;
ALTER TABLE users ADD CONSTRAINT fk_users_primary_client
    FOREIGN KEY (primary_client_id) REFERENCES clients(id) ON DELETE SET NULL;
CREATE INDEX ix_users_primary_client_id ON users(primary_client_id);
```

---

## 📡 ENDPOINTS IMPLEMENTADOS

### **Clientes**

#### `POST /api/v1/clients`
Cria cliente com criação opcional de usuário.

**Request:**
```json
{
  "razao_social": "Tech Solutions Ltda",
  "cnpj": "12.345.678/0001-90",
  "email": "contato@techsolutions.com",
  "honorarios_mensais": 800,
  "dia_vencimento": 10,
  "regime_tributario": "simples_nacional",
  "tipo_empresa": "servico",
  "create_user": true,
  "user_email": "roberto@techsolutions.com",
  "user_name": "Roberto Costa"
}
```

**Response:** `201 Created`
```json
{
  "client": {
    "id": "uuid",
    "razao_social": "Tech Solutions Ltda",
    ...
  },
  "user_created": true,
  "user_email": "roberto@techsolutions.com",
  "temporary_password": "Xy3#jK8@pL2m"
}
```

#### `POST /api/v1/clients/{client_id}/users`
Vincula usuário existente a cliente.

**Request:**
```json
{
  "user_id": "uuid",
  "access_level": "MANAGER"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "message": "User linked to client successfully"
}
```

---

### **Usuários**

#### `GET /api/v1/users` (Admin only)
Lista usuários com filtros e paginação.

**Query Parameters:**
- `query` (opcional): Busca por nome ou email
- `role` (opcional): Filtro por role (admin, func, cliente)
- `is_active` (opcional): Filtro por status ativo (true/false)
- `page` (padrão: 1): Número da página
- `size` (padrão: 10): Tamanho da página

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "João Silva - Contador",
      "email": "func@contabil.com",
      "role": "func",
      "is_active": true,
      "is_verified": true,
      "last_login_at": "2025-11-10T14:30:00Z",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-11-10T14:30:00Z"
    }
  ],
  "total": 10,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

#### `POST /api/v1/users` (Admin only)
Cria novo usuário.

**Request:**
```json
{
  "name": "Maria Santos",
  "email": "maria@contabil.com",
  "password": "senha123",
  "role": "func"
}
```

#### `PUT /api/v1/users/{user_id}`
Atualiza usuário (admin ou próprio usuário).

**Request:**
```json
{
  "name": "Maria Santos Silva",
  "email": "maria.santos@contabil.com",
  "role": "admin",
  "is_active": true
}
```

**Regras:**
- Admin pode alterar qualquer campo
- Usuário comum só pode alterar `name` e `email`

#### `PATCH /api/v1/users/{user_id}/activate` (Admin only)
Ativa usuário desativado.

#### `PATCH /api/v1/users/{user_id}/deactivate` (Admin only)
Desativa usuário.

#### `POST /api/v1/users/{user_id}/reset-password` (Admin only)
Reseta senha do usuário.

**Request:**
```json
{
  "generate_temporary": true
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "temporary_password": "aB3#kL9@xM5p",
  "message": "Password reset successfully"
}
```

**Ou:**
```json
{
  "generate_temporary": false,
  "new_password": "novaSenha123"
}
```

---

## 🏗️ ARQUITETURA

### **Models**

#### `ClientUser` ([client_user.py](../app/db/models/client_user.py))
```python
class ClientAccessLevel(str, Enum):
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    VIEWER = "VIEWER"

class ClientUser(Base, UUIDMixin, TimestampMixin):
    client_id: Mapped[UUID]
    user_id: Mapped[UUID]
    access_level: Mapped[ClientAccessLevel]

    # Relationships
    client = relationship("Client", back_populates="client_users")
    user = relationship("User", back_populates="client_users")
```

#### Atualizações em `User` e `Client`
- `User.primary_client_id`: FK para acesso rápido ao cliente principal
- `User.client_users`: Relacionamento com `ClientUser`
- `Client.client_users`: Relacionamento com `ClientUser`

---

### **Repositories**

#### `UserRepository` ([user.py](../app/db/repositories/user.py))
```python
class UserRepository(BaseRepository[User]):
    async def get_by_email(email: str) -> User | None
    async def email_exists(email: str, exclude_id: UUID | None) -> bool
    async def list_with_filters(
        query: str | None,
        role: UserRole | None,
        is_active: bool | None,
        skip: int,
        limit: int
    ) -> tuple[list[User], int]
    async def get_users_by_client(client_id: UUID) -> list[User]
    async def activate(user: User) -> User
    async def deactivate(user: User) -> User
```

---

### **Services**

#### `ClientService` ([client.py](../app/services/client.py))
**Método atualizado:**
```python
async def create_client(
    client_data: ClientCreate
) -> ClientCreateResponse:
    """
    Cria cliente e opcionalmente cria usuário automaticamente.

    Fluxo:
    1. Valida CNPJ único
    2. Cria cliente
    3. Se create_user=True:
       - Determina email (user_email > responsavel_email > email)
       - Determina nome (user_name > responsavel_nome > razao_social)
       - Gera senha temporária segura
       - Cria User com role=CLIENTE
       - Cria ClientUser com access_level=OWNER
       - Define primary_client_id
    4. Retorna ClientCreateResponse com credenciais
    """
```

#### `UserService` ([user.py](../app/services/user.py))
```python
class UserService:
    async def create_user(user_data: UserCreate) -> UserResponse
    async def get_user(user_id: UUID) -> UserResponse
    async def update_user(user_id: UUID, user_data: UserUpdate) -> UserResponse
    async def activate_user(user_id: UUID) -> None
    async def deactivate_user(user_id: UUID) -> None
    async def list_users(
        query: str | None,
        role: str | None,
        is_active: bool | None,
        page: int,
        size: int
    ) -> dict
    async def reset_password(
        user_id: UUID,
        reset_data: UserResetPasswordRequest
    ) -> UserResetPasswordResponse
    async def link_user_to_client(
        client_id: UUID,
        user_id: UUID,
        access_level: ClientAccessLevel
    ) -> None
```

---

### **Schemas**

#### `ClientCreateResponse` ([client.py](../app/schemas/client.py))
```python
class ClientCreateResponse(BaseSchema):
    client: ClientResponse
    user_created: bool = False
    user_email: str | None = None
    temporary_password: str | None = None
```

#### Novos schemas de User ([user.py](../app/schemas/user.py))
```python
class UserListItem(TimestampSchema):
    id: UUID
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    last_login_at: datetime | None

class UserResetPasswordRequest(BaseSchema):
    generate_temporary: bool = True
    new_password: str | None = None

class UserResetPasswordResponse(BaseSchema):
    success: bool
    temporary_password: str | None
    message: str
```

---

## 🔐 SEGURANÇA

### **Geração de Senha Temporária**
```python
def _generate_temporary_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password
```

**Características:**
- 12 caracteres
- Mix de letras (maiúsculas/minúsculas), números e símbolos
- Usa `secrets` (cryptographically strong)

### **RBAC (Role-Based Access Control)**

| Endpoint | Admin | Func | Cliente |
|----------|-------|------|---------|
| `POST /clients` | ✅ | ✅ | ❌ |
| `POST /clients/:id/users` | ✅ | ✅ | ❌ |
| `GET /users` | ✅ | ❌ | ❌ |
| `POST /users` | ✅ | ❌ | ❌ |
| `PUT /users/:id` | ✅ (all) | ❌ | ✅ (self only) |
| `PATCH /users/:id/activate` | ✅ | ❌ | ❌ |
| `POST /users/:id/reset-password` | ✅ | ❌ | ❌ |

---

## 🌱 SEEDS

### Comando:
```bash
cd apps/api
venv/Scripts/python.exe -m scripts.seed_users
```

### Usuários criados:
```
Admins (2):
  - admin@contabil.com / admin123
  - admin2@contabil.com / admin123

Funcionários (3):
  - func@contabil.com / func123 (Contador)
  - func2@contabil.com / func123 (Assistente)
  - func3@contabil.com / func123 (Analista Fiscal)

Clientes (5):
  - contato@techsolutions.com / cliente123
  - comercial@supermercadoboa.com / cliente123
  - admin@restaurantegirassol.com / cliente123
  - financeiro@construtoranovavida.com / cliente123
  - contato@belezaecia.com / cliente123
```

---

## 🧪 TESTES MANUAIS

### 1. Criar cliente com usuário automático
```bash
curl -X POST http://localhost:8000/api/v1/clients \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "razao_social": "Empresa Teste Ltda",
    "cnpj": "12.345.678/0001-90",
    "email": "contato@teste.com",
    "honorarios_mensais": 500,
    "dia_vencimento": 10,
    "regime_tributario": "simples_nacional",
    "tipo_empresa": "servico",
    "create_user": true
  }'
```

**Verificar:**
- ✅ Cliente criado
- ✅ Usuário criado com role CLIENTE
- ✅ Relacionamento `client_users` criado com OWNER
- ✅ Senha temporária retornada

### 2. Listar usuários
```bash
curl http://localhost:8000/api/v1/users?role=cliente&page=1&size=10 \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### 3. Resetar senha
```bash
curl -X POST http://localhost:8000/api/v1/users/{user_id}/reset-password \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"generate_temporary": true}'
```

---

## 📊 ESTATÍSTICAS

- **Arquivos criados**: 2
- **Arquivos modificados**: 8
- **Linhas de código**: ~800
- **Endpoints adicionados**: 6
- **Migrations**: 1
- **Tempo de desenvolvimento**: ~4 horas

---

## 🚀 PRÓXIMOS PASSOS (FASE 2)

### Frontend - Módulo de Configurações

1. **Página `/configuracoes`**
   - Tab "Usuários"
   - Tab "Sistema"
   - Tab "Perfil"

2. **Componentes**
   - `UsersTable.tsx` - Tabela de usuários
   - `UserFormModal.tsx` - Modal criar/editar
   - `UserRoleChip.tsx` - Badge de role
   - `UserStatusChip.tsx` - Badge de status

3. **Hooks**
   - `useUsers.ts` - Gerenciamento de estado

4. **API Client**
   - `apps/web/src/lib/api/endpoints/users.ts`

---

## 📝 NOTAS IMPORTANTES

1. **Senha Temporária**: Deve ser alterada no primeiro login (implementar no frontend)
2. **Email Notifications**: Implementar envio de email com credenciais (futuro)
3. **Primary Client**: Usuário pode ter múltiplos clientes, mas apenas um primário
4. **Soft Delete**: Implementar soft delete para usuários (futuro)

---

## 🎉 CONCLUSÃO

Fase 1 **100% COMPLETA** com implementação robusta de:
- Sistema de relacionamento Cliente ↔ Usuário
- Criação automática de usuário ao cadastrar cliente
- CRUD completo de usuários com RBAC
- Seeds realistas para demonstração

**Ready for Production Backend!** 🚀
